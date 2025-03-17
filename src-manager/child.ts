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

const desktopWin = new WebviewWindow('desktop', {
  url: 'desktop.html',
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

desktopWin.once('tauri://error', async (error: any) => {
  // 有问题优先检查 error，一般是权限不够
  console.log(error)
})

const openDesktop = () => {  // 异步会让 alwaysOnBottom 失效
  desktopWin.show()  // 权限是 core:window:allow-show 而不是 core:webview:allow-webview-show
  desktopWin.setAlwaysOnBottom(true)  // alwaysOnBottom: true 属性不生效，用 setAlwaysOnBottom(true) 函数置底
  desktopWin.setAlwaysOnBottom(true)  // 第一次调用可能无法生效，调用两次即可
}
// 注：setAlwaysOnBottom 会让某些组件异常


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
openDesktop()  // 在其他文件调用会使 alwaysOnBottom 失效
spawnServer()

// 关闭
import { listen } from '@tauri-apps/api/event'

listen('quit', (event) => {
  exitDeskset()
})

const exitDeskset = () => {  // 异步可能无法关闭窗口
  killServer()
  floatManager.closeAll()
  desktopWin.close()
  managerWin.close()
}

managerWin.once('tauri://close-requested', () => {
  managerWin.hide()
})

// 更新
export const updateDeskset = async (url: string) => {
  const updater = Command.sidecar('DesksetUpdater', ['-url', url])
  killServer()
  await desktopWin.close()
  await updater.execute()
}
