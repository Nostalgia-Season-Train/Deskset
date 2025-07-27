import { readDir, readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'


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
  try {
    const text = await readTextFile(`./widgets/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })

    const info = JSON.parse(text)
    return {
      author: typeof info?.author == 'string' ? info.author as string : '未知',
      version: typeof info?.version == 'string' ? info.version as string : '未知',
      descript: typeof info?.descript == 'string' ? info.descript as string : '未知'
    }
  } catch (err) {
    logError('Get widget metainfo fail: ' + (err as Error).message)
  } finally {
    return {
      author: '未知',
      version: '未知',
      descript: '未知'
    }
  }
}
