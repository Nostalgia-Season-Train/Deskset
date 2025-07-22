import { readDir, BaseDirectory } from '@tauri-apps/plugin-fs'


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
