import {
  readDir,
  mkdir,
  readTextFile,
  writeTextFile,
  remove,
  BaseDirectory
} from '@tauri-apps/plugin-fs'
import { Theme } from '#manager/global/theme.ts'  // #manager/global 找不到类型声明？原因？


/* === 遍历主题 === */
export const getThemes = async () => {
  const entrys = await readDir('./themes', { baseDir: BaseDirectory.Resource })

  let themes: Theme[] = []
  for (const entry of entrys) {
    if (entry.isDirectory == false)
      continue
    const name = entry.name
    const infoText = await readTextFile(`./themes/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })
    const info = JSON.parse(infoText)
    themes.push({
      name: name,
      savetime: info?.savetime ?? '',
      descript: info?.descript ?? ''
    })
  }
  return themes
}


/* === 保存主题 === */
export const saveTheme = async (name: string, data: object, info: object) => {
  const dataText = JSON.stringify(data, null, 2)
  const infoText = JSON.stringify(info, null, 2)
  await mkdir(`./themes/${name}`, { baseDir: BaseDirectory.Resource, recursive: true })
  await writeTextFile(`./themes/${name}/data.json`, dataText, { baseDir: BaseDirectory.Resource })
  await writeTextFile(`./themes/${name}/metainfo.json`, infoText, { baseDir: BaseDirectory.Resource })
}


/* === 删除主题 === */
export const deleteTheme = async (name: string) => {
  await remove(`./themes/${name}`, { baseDir: BaseDirectory.Resource, recursive: true })
}


/* === 读取主题数据 data.json === */
export const readThemeData = async (name: string) => {
  const dataText = await readTextFile(`./themes/${name}/data.json`, { baseDir: BaseDirectory.Resource })
  const data = JSON.parse(dataText)
  return data
}
