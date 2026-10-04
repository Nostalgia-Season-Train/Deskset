/* ==== 部件类 Widgetcls ==== */
// - 备选名：部件模板、部件蓝图
// - 作用：1个 部件类 就是 1个 Vue组件，可以构造 N个 部件

/* --- 部件类标识 --- */
// - 作用：标识是哪个部件类
export interface WidgetclsID {
  // 部件路径
  path: string
  // 部件内联标识
  // - 内联部件是提前写好并打包进数字桌搭的部件
  // - 附：be 代表特殊布尔属性区分 is
  beInline: boolean
}

/* --- 部件类注册值 --- */
// - 作用：通过 json 文件定义的部件类元数据
export interface WidgetclsInfo {
  // 部件（类）信息
  name: string      // 部件名称
  author: string    // 部件作者
  version: string   // 部件版本
  descript: string  // 部件描述
}
export interface WidgetclsRegv extends WidgetclsInfo {
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

/* --- 部件类 --- */
export interface Widgetcls extends WidgetclsID, WidgetclsRegv {
  // 部件主函数
  // - 编译出的 Vue SFC 代码函数
  // - 使用方法：const vnode = h({ render: main }); render(vnode, el)
  main: Function
  // - [ ] 待定：部件模型验证
  modelValidate?: unknown
  // - [ ] 待定：部件选项组件
  optionComponent?: unknown
}


/* ==== 部件 Widget ==== */

/* --- 部件标识 --- */
export interface WidgetID extends WidgetclsID {
  id: string         // 部件（实例）唯一标识符
  path: string       // 同部件（类）路径
  beInline: boolean  // 同部件（类）内联标识
}

/* --- 部件 --- */
export interface Widget extends WidgetID {
  // 部件标题
  // - 默认等于部件名称
  // - 附：只在管理页显示，但为了方便逻辑，跟其他属性一样在桌面页存储
  title: string

  // 部件 CSS 类名
  // - 作用：切换 CSS 类名以改变部件（容器）状态
  isDragLock: boolean         // 部件是否锁定拖动
  isDisableInteract: boolean  // 部件是否禁用交互（事件）
  isAutoHide: boolean         // 部件是否自动隐藏（鼠标移入时显示）

  // 部件 CSS 属性
  // - 作用：设置 CSS 属性以改变部件（容器）偏移/位置、缩放/大小、不透明度/透明度
  left: number     // 部件向右偏移
  top: number      // 部件向下偏移
  scale: number    // 部件缩放
  opacity: number  // 部件不透明度

  // 部件坐标
  // - 注 1：区分于 left、top，x、y 是部件中心到左上角的距离
  // - 注 2：部件实际位置由 left、top 决定，x、y 仅用于展示
  x: number
  y: number

  // 部件模型
  // - 哪怕部件类没有模型定义，也会创建一个空对象（Object.create(null)）用以占位
  model: Record<string, any>
}
