/* ==== 部件类 Widgetcls ==== */
export interface Widgetcls {
  // 部件路径
  path: string
  // 部件内联标识
  // - 内联部件是提前写好并打包进数字桌搭的部件
  // - 附：be 代表特殊布尔属性区分 is
  beInline: boolean

  // 部件主函数
  // - 编译出的 Vue 组件函数
  main: Function

  name: string      // 部件名称
  author: string    // 部件作者
  version: string   // 部件版本
  descript: string  // 部件描述

  // 部件模型定义
  // - 实例化为部件模型 model
  modelDef?: Record<string, {
    type: string  // 类型
    default: any  // 默认值
  }>
  // 部件选项定义，用于编辑模型
  // - 实例化为部件选项 option（编辑面板组件）
  optionDef?: {
    unknown: unknown  // - [ ] 待定
  }[]
}


/* ==== 部件 Widget ==== */
export interface StorageWidget {
  id: string         // 部件（实例）唯一标识符
  path: string       // 同部件（类）路径
  beInline: boolean  // 同部件（类）内联标识

  // 部件标题
  // - 默认等于部件名称
  // - 附：只在管理页显示，但为了方便逻辑，跟其他属性一样在桌面页存储
  title: string

  isDragLock: boolean         // 部件是否锁定拖动
  isDisableInteract: boolean  // 部件是否禁用交互（事件）
  isAutoHide: boolean         // 部件是否自动隐藏（鼠标移入时显示）

  left: number     // 部件向右偏移
  top: number      // 部件向下偏移
  scale: number    // 部件缩放
  opacity: number  // 部件不透明度

  // 部件模型
  model: Record<string, any>
}
export interface RuntimeWidget extends StorageWidget {
  // 部件坐标
  // - 注意区分 left、top，x、y 是部件中心到左上角的距离
  x: number
  y: number

  // 部件选项
  option?: unknown
}
