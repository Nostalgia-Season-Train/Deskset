import { WebviewWindow } from '@tauri-apps/api/webviewWindow'
import { currentMonitor } from '@tauri-apps/api/window'

const monitor = await currentMonitor()
const width = monitor?.size.width
const height = monitor?.size.height

const desktopWin = new WebviewWindow('desktop', {
  url: 'desktop.html',

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


/* === 打开桌面 === */
const openDesktop = () => {  // 异步会让 alwaysOnBottom 失效
  desktopWin.show()  // 权限是 core:window:allow-show 而不是 core:webview:allow-webview-show
  desktopWin.setAlwaysOnBottom(true)  // alwaysOnBottom: true 属性不生效，用 setAlwaysOnBottom(true) 函数置底
  desktopWin.setAlwaysOnBottom(true)  // 第一次调用可能无法生效，调用两次即可
}
openDesktop()  // 在其他文件调用会使 alwaysOnBottom 失效


/* === 关闭管理窗的同时关闭桌面窗 === */
import { getCurrentWindow } from '@tauri-apps/api/window'

const managerWin = getCurrentWindow()

managerWin.once('tauri://close-requested', () => {
  desktopWin.close()
  managerWin.close()  // 否则关闭按钮要点两次
})
