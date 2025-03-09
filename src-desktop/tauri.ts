// Resource 是 tauri.exe 所在目录，开发时在 src-tauri/target/debug

/* === 主题 === */

// 创建主题
import { mkdir, writeFile, BaseDirectory } from '@tauri-apps/plugin-fs'

export const saveThemeDir = async (name: string, data: any) => {
  const encoder = new TextEncoder()
  const encodeData = encoder.encode(JSON.stringify(data))
  await mkdir(`./themes/${ name }`, { baseDir: BaseDirectory.Resource, recursive: true })
  await writeFile(`./themes/${ name }/data.json`, encodeData, { baseDir: BaseDirectory.Resource })
}

// 读取主题
import { readFile } from '@tauri-apps/plugin-fs'
import { resourceDir, join } from '@tauri-apps/api/path'
import { convertFileSrc } from '@tauri-apps/api/core'

export const readThemeDir = async (themeName: string): Promise<Object> => { 
  let theme = new Object() as { data: string, style: string | undefined }

  try {
    const data = await readFile(`./themes/${ themeName }/data.json`, { baseDir: BaseDirectory.Resource })
    theme.data = JSON.parse(new TextDecoder().decode(data))
  } catch {}

  try {
    const style = await readFile(`./themes/${ themeName }/style.css`, { baseDir: BaseDirectory.Resource })
    const stylePath = await join(await resourceDir(), 'themes', themeName, 'style.css')
    theme.style = convertFileSrc(stylePath)
  } catch (error) {}

  return theme
}
