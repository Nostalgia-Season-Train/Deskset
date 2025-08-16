/* === 打开默认浏览器 === */
import { openUrl } from '@tauri-apps/plugin-opener'

export const openBrowser = async (url: string) => openUrl(url)


/* === 退出数字桌搭 === */
import { error as logError } from '@tauri-apps/plugin-log'

import { LATEST_THEME } from '#manager/global/theme'
import { saveTheme } from './theme'
import { config } from '#manager/global/config'
import { writeConfFile } from './config'
import { killServe } from '#manager/global/child/server'
import { getAllWindows } from '@tauri-apps/api/window'

import { exit } from '@tauri-apps/plugin-process'

export const exitDeskset = async () => {
  // 保存当前部件列表
  await saveTheme(LATEST_THEME)

  // 写入持久化配置
  writeConfFile({
    language: config.language,
    closeBehavior: config.closeBehavior
  })

  // 关闭服务器
  try {
    await killServe()
  } catch (err) {
    logError(`While exiting, a error occur: ${err}`)
  }

  // - [ ] 临时：直接退出，关闭窗口可能卡住
  await exit(0)
  return

  // 关闭所有窗口
  for (const win of await getAllWindows()) {
    try {
      await win.destroy()  // close 不一定能关闭窗口
    } catch (err) {
      logError(`While exiting, a error occur: ${err}`)
    }
  }

  // 如果上面执行完后，没有自然退出。那就通过 exit 强行结束进程
  await exit(0)
}
