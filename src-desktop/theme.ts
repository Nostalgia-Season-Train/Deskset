// Resource 是 tauri.exe 所在目录，开发时在 src-tauri/target/debug

/* === 主题创建 === */
import { mkdir, writeFile, BaseDirectory } from '@tauri-apps/plugin-fs'

export const saveThemeDir = async (name: string, data: any) => {
  const encoder = new TextEncoder()
  const encodeData = encoder.encode(JSON.stringify(data))
  await mkdir(`./themes/${ name }`, { baseDir: BaseDirectory.Resource })
  await writeFile(`./themes/${ name }/data.json`, encodeData, { baseDir: BaseDirectory.Resource })
}
