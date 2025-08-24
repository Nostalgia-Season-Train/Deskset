import { _t } from './i18n'
import { readDir, readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'


/* === 从 widget 库：返回部件名称列表 === */
export const getWidgetNameList = async (): Promise<string[]> => {
  const entrys = await readDir('./widgets', { baseDir: BaseDirectory.Resource })

  let widgetNameList = []
  for (const entry of entrys) {
    if (entry.isDirectory)
      widgetNameList.push(entry.name)
  }
  return widgetNameList
}


/* === 从 widget 库：返回部件信息（元数据） === */
export const getWidgetInfo = async (name: string) => {
  try {
    const text = await readTextFile(`./widgets/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })

    const info = JSON.parse(text)
    return {
      author: typeof info?.author == 'string' ? info.author as string : _t('未知'),
      version: typeof info?.version == 'string' ? info.version as string : _t('未知'),
      descript: typeof info?.descript == 'string' ? info.descript as string : _t('未知'),
      options: null
    }
  } catch (err) {
    logError('Get widget metainfo fail: ' + (err as Error).message)
    return {
      author: _t('未知'),
      version: _t('未知'),
      descript: _t('未知'),
      options: null
    }
  }
}


/* === 添加部件 === */
import desktop from '#manager/global/page/desktop'
import { activeWidgetMap } from '#manager/global'
import { inlineRawWidgetMap, prefixMark } from '#widget/register'

export const appendWidget = async (
  // 部件名称
  name: string,

  // 用于桌面页：部件属性、位置、配置
  isDragLock: boolean | null = null,
  isDisableInteract: boolean | null = null,
  isAutoHide: boolean | null = null,
  left: number | null = null,
  top: number | null = null,
  scale: number | null = null,
  model: Record<string, any> = {},

  // 用于管理页：部件标题（用户自定义，默认等于部件名称）
  title: string | null = null
) => {
  // 1、生成 ID
  let id = Math.random().toString(16).slice(2)

  while (true) {
    if (!activeWidgetMap.has(id))
      break
    id = Math.random().toString(16).slice(2)
  }

  // 2、获取部件信息（元数据）
  const widgetInfo = name.startsWith(prefixMark) ? {
    author: _t(inlineRawWidgetMap.get(name)!.metainfo.author),
    version: inlineRawWidgetMap.get(name)!.metainfo.version,
    descript: _t(inlineRawWidgetMap.get(name)!.metainfo.descript),
    options: inlineRawWidgetMap.get(name)!.metainfo?.options ?? null
  } : await getWidgetInfo(name)

  // 3、桌面添加部件 > 返回部件数据
  const widgetData = await desktop.appendWidget(
    id,
    name, {
      isDragLock: isDragLock,
      isDisableInteract: isDisableInteract,
      isAutoHide: isAutoHide,
      left: left,
      top: top,
      scale: scale,
      model: model
    }
  )

  // 4、记录部件
  activeWidgetMap.set(id, {
    id: id,

    title: title ?? name.startsWith(prefixMark) ? _t(name.replace(prefixMark, '')) : name,
    name: name,

    author: widgetInfo.author,
    version: widgetInfo.version,
    descript: widgetInfo.descript,

    isDragLock: widgetData.isDragLock,
    isDisableInteract: widgetData.isDisableInteract,
    isAutoHide: widgetData.isAutoHide,

    x: widgetData.x,
    y: widgetData.y,

    left: widgetData.left,
    top: widgetData.top,
    scale: widgetData.scale,

    model: widgetData.model,
    options: widgetInfo.options
  })
}
