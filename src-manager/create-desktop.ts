import { WebviewWindow } from '@tauri-apps/api/webviewWindow'

const desktopWin = new WebviewWindow('desktop', {
  url: 'desktop.html'
})

desktopWin.once('tauri://error', async (error: any) => {
  // 有问题优先检查 error，一般是权限不够
  console.log(error)
})


/* === 打开桌面 === */
const openDesktop = async () => {
  desktopWin.show()  // 权限是 core:window:allow-show 而不是 core:webview:allow-webview-show
}
openDesktop()
