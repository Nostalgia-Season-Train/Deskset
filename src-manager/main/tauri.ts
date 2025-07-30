/* === 打开默认浏览器 === */
import { openUrl } from '@tauri-apps/plugin-opener'

export const openBrowser = async (url: string) => openUrl(url)
