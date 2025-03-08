/* === 欢迎、支持 === */
import { openUrl } from '@tauri-apps/plugin-opener'

export const openBrowser = async (url: string) => openUrl(url)


/* === 主题 === */

// 主题遍历
import { readDir, readFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import { resourceDir, join } from '@tauri-apps/api/path'
import { convertFileSrc } from '@tauri-apps/api/core'

export const getAllThemes = async (): Promise<Array<Object>> => { 
  let themes: Array<Object> = []

  // 读取主题库
  const themesDir = await readDir('./themes', { baseDir: BaseDirectory.Resource })
  for (const themeDir of themesDir) {
    if (themeDir.isDirectory == false) {
      break
    }

    // 读取主题
    let theme = new Object() as { name: string, data: string, preview: any | undefined }

    theme.name = themeDir.name

    try {
      const data = await readFile(`./themes/${ themeDir.name }/data.json`, { baseDir: BaseDirectory.Resource })
      theme.data = JSON.parse(new TextDecoder().decode(data))
    } catch {}

    try {
      const preview = await readFile(`./themes/${ themeDir.name }/preview.png`, { baseDir: BaseDirectory.Resource })
      const previewPath = await join(await resourceDir(), 'themes', themeDir.name, 'preview.png')
      theme.preview = convertFileSrc(previewPath)
    } catch (error) {}

    themes.push(theme)
  }

  return themes
}
