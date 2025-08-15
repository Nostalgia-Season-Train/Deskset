import { reactive, ref } from 'vue'

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

  // 部件配置
  model: Record<string, any>
}

export const activeWidgetMap = reactive(new Map<string, Widget>())

export const activeWidgetOnSelect = ref<Widget | null>(null)  // 选中的部件，在 RightInfo.vue 中操作


/* === 主题格式：恢复用户保存的主题 === */
  // 1、从 activeWidgetMap 转换成主题格式
  // 2、从 theme/data.json 验证并转换成主题格式
export const convertWidgetInTheme = async (data: any) => {
  const name = data?.name
  if (typeof name != 'string')
    return undefined

  return {
    name: name as string,
    title: typeof data?.title == 'string' ? data.title as string : name as string,

    isDragLock: typeof data?.isDragLock == 'boolean' ? data.isDragLock as boolean : false,
    isDisableInteract: typeof data?.isDisableInteract == 'boolean' ? data.isDisableInteract as boolean : false,
    isAutoHide: typeof data?.isAutoHide == 'boolean' ? data.isAutoHide as boolean : false,

    left: typeof data?.left == 'number' ? data.left as number : 0,
    top: typeof data?.top == 'number' ? data.top as number : 0,

    model: Object.prototype.toString.call(data?.model) == '[object Object]' ? data.model as Record<string, any> : {}
  }
}
