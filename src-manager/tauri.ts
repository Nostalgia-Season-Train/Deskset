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

// 删除主题
import { remove } from '@tauri-apps/plugin-fs'

export const deleteThemeDir = async (themeName: string) => {
  remove(`./themes/${ themeName }`, {
    baseDir: BaseDirectory.Resource,
    recursive: true
  })
}


/* === 开发 === */

// 获取服务器 port 和 token
import axios from 'axios'

export const getDesksetReq = async (): Promise<any> => {
  // 读取配置
  const data = await readFile(`./config/deskset.json`, { baseDir: BaseDirectory.Resource })
  const config = JSON.parse(new TextDecoder().decode(data))

  // 获取 port
  const port = config['server-port']

  // 获取 token
  const formData = new FormData()
  formData.append('username', config.username)
  formData.append('password', config.password)

  const repLogin = await axios.post(`http://127.0.0.1:${port}/v0/access/login`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  const token = repLogin.data.access_token

  // 返回 desksetReq
  const desksetReq = axios.create({
    baseURL: `http://127.0.0.1:${port}`,
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return desksetReq
}
