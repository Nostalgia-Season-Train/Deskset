import { reactive } from 'vue'

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
}

export const activeWidgetMap = reactive(new Map<string, Widget>())
