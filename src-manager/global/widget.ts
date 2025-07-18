import { reactive } from 'vue'

export interface Widget {
  id: string

  title: string
  local: string
  descript: string

  type: string
  name: string

  isDragLock: boolean
  isDisableInteract: boolean
  isAutoHide: boolean

  // 中心坐标，不是 left 和 top
  x: number
  y: number
}

export const activeWidgetMap = reactive(new Map<string, Widget>())
