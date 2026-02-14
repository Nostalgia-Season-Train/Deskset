import { _t } from './i18n'
import { readDir, readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'
import { RuntimeWidget, StorageWidget, exampleStorageWidget } from '#manager/global'


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
import { inlineRawWidgetMap, prefixMark } from '#widget/register'

export const getWidgetInfo = async (name: string) => {
  // 内联部件
  if (name.startsWith(prefixMark)) {
    return {
      author: _t(inlineRawWidgetMap.get(name)!.metainfo.author),
      version: inlineRawWidgetMap.get(name)!.metainfo.version,
      descript: _t(inlineRawWidgetMap.get(name)!.metainfo.descript),
      model: inlineRawWidgetMap.get(name)!.metainfo?.model ?? {},
      option: inlineRawWidgetMap.get(name)!.metainfo?.option ?? null
    }
  }

  // 外部部件
  try {
    const text = await readTextFile(`./widgets/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })

    const info = JSON.parse(text)
    return {
      author: typeof info?.author == 'string' ? info.author as string : _t('未知'),
      version: typeof info?.version == 'string' ? info.version as string : _t('未知'),
      descript: typeof info?.descript == 'string' ? info.descript as string : _t('未知'),
      model: {},
      option: null
    }
  } catch (err) {
    logError('Get widget metainfo fail: ' + (err as Error).message)
    return {
      author: _t('未知'),
      version: _t('未知'),
      descript: _t('未知'),
      model: {},
      option: null
    }
  }
}


/* === 添加部件 === */
import desktop from '#manager/global/page/desktop'
import { activeWidgetMap } from '#manager/global'

export const appendWidget = async ({
  // 部件名称
  name,

  // 用于桌面页：部件属性、位置、配置
  isDragLock = null,
  isDisableInteract = null,
  isAutoHide = null,
  left = null,
  top = null,
  scale = null,
  model = {},

  // 用于管理页：部件标题（用户自定义，默认等于部件名称）
  title = null
}: {
  name: string,
  isDragLock?: boolean | null,
  isDisableInteract?: boolean | null,
  isAutoHide?: boolean | null,
  left?: number | null,
  top?: number | null,
  scale?: number | null,
  model?: Record<string, any>,
  title?: string | null
}) => {
  // 1、生成 ID
  let id = Math.random().toString(16).slice(2)

  while (true) {
    if (!activeWidgetMap.has(id))
      break
    id = Math.random().toString(16).slice(2)
  }

  // 2、获取部件信息（元数据）
  const widgetInfo = await getWidgetInfo(name)
  const registerModel = widgetInfo.model
  const registerOption = widgetInfo.option

  // 2.1、从（部件）注册模型生成默认模型
  let defaultModel: Record<string, any> = {}
  for (const key of Object.keys(registerModel)) {
    defaultModel[key] = registerModel[key].default  // - [ ] 待处理：动态生成默认值
  }

  // 2.2、从（部件）注册选项和注册模型生成默认选项
    // - [ ] 待处理：优化命名和逻辑
      // 区分 model.key、model.name 和 tab.id(tab.key)、tab.text(tab.name)
      // 一律采用 undefined 判断空值，方便 object.key 语法
  if (registerOption != null) {
    let defaultOption: { items: any[], tabs: any[] | undefined } = { items: [], tabs: undefined }
    for (const item of registerOption.items) {
      defaultOption.items.push({ key: item, ...registerModel[item] })
    }
    if (Array.isArray(registerOption?.tabs)) {
      defaultOption.tabs = []
      for (const tab of registerOption.tabs) {
        let defaultTab = structuredClone({ ...tab, items: [] })  // 不要 tab.items，重新生成
        for (const item of tab.items) {
          defaultTab.items.push({ key: item, ...registerModel[item] })
        }
        defaultOption.tabs.push(defaultTab)
      }
    }
    widgetInfo.option = defaultOption
  }

  // 3、桌面添加部件 > 返回部件数据
  let widgetData = null
  try {
    widgetData = await desktop.appendWidget(
      id,
      name, {
        isDragLock: isDragLock,
        isDisableInteract: isDisableInteract,
        isAutoHide: isAutoHide,
        left: left,
        top: top,
        scale: scale,
        model: Object.keys(model).length != 0 ? model : defaultModel  // model 为空则传入默认值
      }
    )
  } catch (err) {
    logError('Append widget fail: ' + (err as Error).message)
    return
  }

  // 4、记录部件
  activeWidgetMap.set(id, Object.assign(
    {
      id: id,
      name: name,
      title: title ?? (name.startsWith(prefixMark) ? _t(name.replace(prefixMark, '')) : name)
    },
    widgetInfo,
    widgetData
  ))
}


/* === 主题格式：恢复用户保存的主题 === */

// 将 运行时部件 转换成 持久化部件
export const RuntimeToStorageWidget = async (widget: RuntimeWidget): Promise<StorageWidget> => {
  let result: Record<string, any> = {}
  for (const key of Object.keys(exampleStorageWidget) as (keyof StorageWidget)[]) {
    result[key] = widget[key]
  }
  return result as StorageWidget
}

// 验证文件中部件，一般来说 文件中部件 = 持久化部件
export const FileToStorageWidget = async (data: any): Promise<StorageWidget | undefined> => {
  const name = data?.name
  if (typeof name != 'string')
    return undefined

  /* --- 补全内联部件配置 --- */
  let model = Object.prototype.toString.call(data?.model) == '[object Object]' ? data.model as Record<string, any> : {}

  // 补全 model 中没有而 defaultModel 中有的键
  const fillMissingKeys = async (
    model: Record<string, any>,
    defaultModel: Record<string, any>
  ): Promise<Record<string, any>> => {
    // const result = { ...model }
    // 上面是错误方法，可能会将内部数组 Record<string, Array> 转换成对象 Record<string, Record<number, Any>>
      // 例如 { filters: [Any] } > { filters: { 0: Any } }
    const result = JSON.parse(JSON.stringify(model))

    for (const key in defaultModel) {
      // 补全缺失的键
      if (!(key in result))
        result[key] = defaultModel[key]
      // 递归处理嵌套对象或数组
      if (typeof result[key] == 'object' && result[key] != null && defaultModel[key] != null)
        result[key] = await fillMissingKeys(result[key], defaultModel[key])
    }

    return result
  }

  if (name.startsWith(prefixMark)) {
    const defaultModel = inlineRawWidgetMap.get(name)!.metainfo?.model ?? {}  // 暂且默认 name 对应部件存在
    model = await fillMissingKeys(model, defaultModel)
  }

  return {
    id: data.id,

    name: name as string,
    title: typeof data?.title == 'string' ? data.title as string : name as string,

    isDragLock: typeof data?.isDragLock == 'boolean' ? data.isDragLock as boolean : false,
    isDisableInteract: typeof data?.isDisableInteract == 'boolean' ? data.isDisableInteract as boolean : false,
    isAutoHide: typeof data?.isAutoHide == 'boolean' ? data.isAutoHide as boolean : false,

    left: typeof data?.left == 'number' ? data.left as number : 0,
    top: typeof data?.top == 'number' ? data.top as number : 0,
    scale: typeof data?.scale == 'number' ? data.scale as number : 1,

    model: model
  }
}
