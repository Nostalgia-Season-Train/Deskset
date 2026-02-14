import { reactive, ref } from 'vue'

export interface StorageWidget {
  id: string

  title: string  // 标题：用户可以自定义标题，默认等于 name 属性
  name: string   // 名称：一个目录存放一个部件，部件名 = 目录名

  isDragLock: boolean
  isDisableInteract: boolean
  isAutoHide: boolean

  // 实际偏移，用于应用主题时设置部件位置
  left: number
  top: number
  scale: number  // 缩放

  // （部件）模型，也就是部件的配置
  model: Record<string, any>
}

export interface RuntimeWidget extends StorageWidget {
  // 由部件目录下 metainfo.json 声明
  author: string  // 作者
  version: string  // 版本
  descript: string  // 描述

  // 中心坐标，不是 left 和 top
  x: number
  y: number

  // （部件模型）选项，定义 routers.Widget.EditMenu 如何编辑 widget.model
  option: { items: any[], tabs: any[] | undefined } | undefined
}

export const activeWidgetMap = reactive(new Map<string, RuntimeWidget>())

export const activeWidgetOnSelect = ref<RuntimeWidget | null>(null)  // 选中的部件，在 RightInfo.vue 中操作

// 相当于运行期类型声明，方便函数自动将 RuntimeWidget 转换成 StorageWidget
export const exampleStorageWidget: StorageWidget = {
  id: '',
  title: '',
  name: '',
  isDragLock: false,
  isDisableInteract: false,
  isAutoHide: false,
  left: 0,
  top: 0,
  scale: 0,
  model: {}
}
