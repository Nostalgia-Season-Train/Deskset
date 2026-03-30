import { reactive, ref } from 'vue'

export interface RegisterModelOptionItem {
  key: string                      // 选项要修改的 model.key
  input: string                    // 用哪个组件修改
  parameter?: Record<string, any>  // 传递给选项组件的参数（选项组件的配置）
  name?: string      // 选项名称
  descript?: string  // 选项描述
}

// 部件类 Widgetcls 标识符
export interface WidgetclsID {
  path: string       // 路径：比如 note/base 就是内联部件数据库的路径（src-widget/note/base.vue）
  beInline: boolean  // 是否内联，be 代表特殊布尔属性区分 is
}
// Widgetcls 命名相比 WidgetClass 更能区分 Widget，说明是两种类型
export interface Widgetcls extends WidgetclsID {
  main: Function  // 动态导入内联部件的函数，返回 Promise（仅在桌面窗口使用）

  name: string
  author: string
  version: string
  descript: string

  model?: Record<string, {
    type: string,
    default: any
  }>

  option?: {
    items: RegisterModelOptionItem[]
    tabs: {
      id: string
      text: string
      items: RegisterModelOptionItem[]
    }[]
  }
}

// 部件实例 Widget 标识符（标识符在添加部件时必须带上）
export interface StorageWidgetID extends WidgetclsID {
  id: string
}
export interface StorageWidget extends StorageWidgetID {
  title: string  // 标题：用户可以自定义标题，默认等于 name 属性（仅在桌面窗口使用）

  isDragLock: boolean
  isDisableInteract: boolean
  isAutoHide: boolean

  // 实际偏移，用于应用主题时设置部件位置
  left: number
  top: number
  scale: number  // 缩放
  opacity: number  // 不透明度

  // （部件）模型，也就是部件的配置
  model: Record<string, any>
}
export interface RuntimeWidget extends StorageWidget {
  // 由部件目录下 metainfo.json 声明
  name: string      // 名称
  author: string    // 作者
  version: string   // 版本
  descript: string  // 描述

  // 中心坐标，不是 left 和 top
  x: number
  y: number

  // （部件模型）选项，定义 routers.Widget.EditMenu 如何编辑 widget.model
  option?: Widgetcls['option']
}

export const activeWidgetMap = reactive(new Map<string, RuntimeWidget>())

export const activeWidgetOnSelect = ref<RuntimeWidget | null>(null)  // 选中的部件，在 RightInfo.vue 中操作

// 相当于运行期类型声明，方便函数自动将 RuntimeWidget 转换成 StorageWidget
export const exampleStorageWidget: StorageWidget = {
  id: '',
  path: '',
  beInline: true,
  title: '',
  isDragLock: false,
  isDisableInteract: false,
  isAutoHide: false,
  left: 0,
  top: 0,
  scale: 1,
  opacity: 1,
  model: {}
}


/* ==== 部件类列表 ==== */
import { _t } from '#manager/main/i18n'

/* --- 内联部件类 --- */
import { inlineWidgetclsMap as rawInlineWidgetclsMap } from '#widget/register'
// 添加类型
const _inlineWidgetclsMap = rawInlineWidgetclsMap as Map<string, Widgetcls>
// 翻译内联部件类的名称、作者和描述
for (const widgetClass of _inlineWidgetclsMap.values()) {
  for (const key in widgetClass)
    if (key === 'name' || key === 'author' || key === 'descript')
      widgetClass[key] = _t(widgetClass[key])
}
export const inlineWidgetclsMap = _inlineWidgetclsMap

/* --- 外部部件类 --- */
import { readDir, readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'

const listVueFilepaths = async (vueDirpath: string) => {
  let vueFilepaths: string[] = []
  for (const entry of await readDir(vueDirpath, { baseDir: BaseDirectory.Resource })) {
    if (entry.isFile && entry.name.endsWith('.vue'))
      vueFilepaths.push(`${vueDirpath}/${entry.name}`)
    if (entry.isDirectory)
      vueFilepaths = [...vueFilepaths, ...await listVueFilepaths(`${vueDirpath}/${entry.name}`)]
  }
  return vueFilepaths
}

const readWidgetInfo = async (path: string) => {
  try {
    const info = JSON.parse(await readTextFile(`./widgets/${path}.json`, { baseDir: BaseDirectory.Resource }))
    return {
      name: typeof info?.name == 'string' ? info.name as string : _t('未知'),
      author: typeof info?.author == 'string' ? info.author as string : _t('未知'),
      version: typeof info?.version == 'string' ? info.version as string : _t('未知'),
      descript: typeof info?.descript == 'string' ? info.descript as string : _t('未知'),
      model: Object.create(null),
      option: undefined
    }
  } catch (err) {
    logError('Get widget metainfo fail: ' + (err as Error).message)
    return {
      name: _t('未知'),
      author: _t('未知'),
      version: _t('未知'),
      descript: _t('未知'),
      model: Object.create(null),
      option: undefined
    }
  }
}

const WIDGET_LIB = 'widgets'

const _outsideWidgetclsMap: Map<string, Widgetcls> = new Map()
for (const sfcpath of await listVueFilepaths(WIDGET_LIB)) {
  const path = sfcpath.slice(`${WIDGET_LIB}/`.length, -'.vue'.length)
  _outsideWidgetclsMap.set(path, {
    main: () => { },
    path: path,
    beInline: false,
    ...await readWidgetInfo(path)
  })
}
export const outsideWidgetclsMap = _outsideWidgetclsMap
