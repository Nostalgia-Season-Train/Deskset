import { readDir, readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs'


/* === 返回部件名称列表 === */
export const getWidgetNameList = async (): Promise<string[]> => {
  const entrys = await readDir('./widgets', { baseDir: BaseDirectory.Resource })

  let widgetNameList = []
  for (const entry of entrys) {
    if (entry.isDirectory)
      widgetNameList.push(entry.name)
  }
  return widgetNameList
}


/* === 返回部件信息（元数据） === */
export const getWidgetInfo = async (name: string) => {
  const text = await readTextFile(`./widgets/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })

  const info = JSON.parse(text)
  return {
    author: info?.author,
    version: info?.version,
    descript: info?.descript
  }
}
