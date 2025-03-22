/* === 后端程序 DesksetBack.exe === */
import { Command, Child } from '@tauri-apps/plugin-shell'

let server: Child | undefined = undefined

const spawnServer = async (): Promise<void> => {
  const command = Command.sidecar('DesksetBack')
  server = await command.spawn()
}

const killServer = (): void => {
  if (server != undefined) {
    server.kill()
  }
}


/* === 桌面窗口 Deskset-Desktop === */
import { WebviewWindow } from '@tauri-apps/api/webviewWindow'
import { currentMonitor } from '@tauri-apps/api/window'

const monitor = await currentMonitor()
const width = monitor?.size.width
const height = monitor?.size.height

class DesktopManager {
  private desktop: WebviewWindow | undefined
  private currentDesktopName: string

  constructor() {
    this.choose('')
  }

  // 当前桌面
  current = () => {
    return this.currentDesktopName
  }

  // 选择桌面
  choose = async (desktopName: string) => {
    // 桌面若打开，则关闭以重新创建
    const desktop = await WebviewWindow.getByLabel('desktop')
    if (desktop != null) {
      await desktop.close()
    }

    // 创建桌面
    this.desktop = new WebviewWindow('desktop', {
      url: `desktop.html#/${desktopName}`,
      title: 'Deskset-Desktop',

      transparent: true,
      decorations: false,
      shadow: false,  // 去掉边缘阴影
      skipTaskbar: true,

      // fullscreen 有不少问题，直接设置宽高
      x: 0,
      y: 0,
      width: width,
      height: height,
      resizable: false,

      focus: false  // 聚焦会改变窗口 z 序，破坏 alwaysOnBottom
    })
    this.currentDesktopName = desktopName

    // 桌面置底
    this.desktop.show()
    this.desktop.setAlwaysOnBottom(true)
    this.desktop.setAlwaysOnBottom(true)  // 第一次调用可能无法生效，调用两次即可

    // 打印报错，方便调试
    this.desktop.once('tauri://error', async (error: any) => {
      // 有问题优先检查 error，一般是权限不够
      console.log(error)
    })
  }

  close = async () => {
    this.desktop?.close()
  }
}

export const desktopManager = new DesktopManager()


/* === 浮动窗口 === */
import { Effect } from '@tauri-apps/api/window'

class FloatManager {
  private floatList: Map<string, WebviewWindow>

  constructor() {
    this.floatList = new Map()
  }

  create = async (page: string, width: number, height: number, alwaysOnTop: boolean = true) => {
    const floatWin = new WebviewWindow(`float:${page}`, {
      url: `float.html#/${page}`,
      title: `Deskset Float ${page}`,
      transparent: true, decorations: false, shadow: false, skipTaskbar: true,
      windowEffects: { effects: [Effect.Blur] },
      alwaysOnTop: alwaysOnTop,
      x: 100, y: 100,
      width: width, height: height,
      resizable: false
    })
    floatWin.once('tauri://error', async (error: any) => { console.log(error) })
    floatWin.show()

    this.floatList.set(page, floatWin)
  }

  close = async (page: string) => {
    const window = this.floatList.get(page)
    await window?.close()
  }

  closeAll = async () => {
    for (const [page, window] of this.floatList) {
      await window.close()
    }
  }
}

export const floatManager = new FloatManager()


/* === 子程序，子窗口 === */
import { getCurrentWindow } from '@tauri-apps/api/window'

const managerWin = getCurrentWindow()

// 打开
spawnServer()

// 关闭
import { listen } from '@tauri-apps/api/event'

listen('quit', (event) => {
  exitDeskset()
})

const exitDeskset = () => {  // 异步可能无法关闭窗口
  killServer()
  floatManager.closeAll()
  desktopManager.close()
  managerWin.close()
}

// 注：通过 Rust 主程序阻止窗口关闭
  // 窗口关闭再打开，将会重置 child.ts 中的变量，导致变量存储的子程序、子窗口句柄丢失
managerWin.once('tauri://close-requested', () => {
  // managerWin.hide()  // 第二次 close-requested 不会 hide 将直接关闭窗口！
  // managerWin.close()    // 所以 close 窗口，让主进程 main.rs 重新创建
})

// 更新
export const updateDeskset = async (url: string) => {
  const updater = Command.sidecar('DesksetUpdater', ['-url', url])
  killServer()
  await desktopManager.close()
  await updater.execute()
}
