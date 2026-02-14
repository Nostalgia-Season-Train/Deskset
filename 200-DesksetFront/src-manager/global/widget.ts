import { reactive, ref } from 'vue'

// - [ ] 待处理：拆分成 StorageWidget 和 RuntimeWidget
export interface Widget {
  id: string

  title: string  // 标题：用户可以自定义标题，默认等于 name 属性
  name: string   // 名称：一个目录存放一个部件，部件名 = 目录名

  // 由部件目录下 metainfo.json 声明
  author: string  // 作者
  version: string  // 版本
  descript: string  // 描述

  isDragLock: boolean
  isDisableInteract: boolean
  isAutoHide: boolean

  // 中心坐标，不是 left 和 top
  x: number
  y: number

  // 实际偏移，用于应用主题时设置部件位置
  left: number
  top: number
  scale: number  // 缩放

  /* --- 部件配置 --- */
  // 配置数据
  model: Record<string, any>
  // 配置选项
  option: { items: any[], tabs: any[] | undefined } | undefined
}

export const activeWidgetMap = reactive(new Map<string, Widget>())

export const activeWidgetOnSelect = ref<Widget | null>(null)  // 选中的部件，在 RightInfo.vue 中操作


/* === 主题格式：恢复用户保存的主题 === */
  // 1、从 activeWidgetMap 转换成主题格式
  // 2、从 theme/data.json 验证并转换成主题格式
import { inlineRawWidgetMap, prefixMark } from '#widget/register'

export const convertWidgetInTheme = async (data: any) => {
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
