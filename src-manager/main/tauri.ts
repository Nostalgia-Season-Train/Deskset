/* === 打开默认浏览器 === */
import { openUrl } from '@tauri-apps/plugin-opener'

export const openBrowser = async (url: string) => openUrl(url)


/* === 退出数字桌搭 === */
import { error as logError } from '@tauri-apps/plugin-log'

import { LATEST_THEME } from '#manager/global/theme'
import { saveTheme } from './theme'
import { killServe } from '#manager/global/child/server'
import { getAllWindows } from '@tauri-apps/api/window'

export const exitDeskset = async () => {
  // 保存当前部件列表
  await saveTheme(LATEST_THEME)

  // 关闭服务器
  try {
    await killServe()
  } catch (err) {
    logError(`While exiting, a error occur: ${err}`)
  }

  // 关闭所有窗口
  for (const win of await getAllWindows()) {
    try {
      await win.close()
    } catch (err) {
      logError(`While exiting, a error occur: ${err}`)
    }
  }
}
