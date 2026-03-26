import { reactive, ref } from 'vue'

export interface RegisterModelOptionItem {
  key: string                      // 选项要修改的 model.key
  input: string                    // 用哪个组件修改
  parameter?: Record<string, any>  // 传递给选项组件的参数（选项组件的配置）
  name?: string      // 选项名称
  descript?: string  // 选项描述
}

export interface WidgetClass {
  path: string
  beInline: boolean

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

export interface StorageWidget {
  id: string
  path: string       // 路径：比如 note/base 就是内联部件数据库的路径（src-widget/note/base.vue）
  beInline: boolean  // 是否内联，be 代表特殊布尔属性区分 is

  title: string  // 标题：用户可以自定义标题，默认等于 name 属性

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
  option?: WidgetClass['option']
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
