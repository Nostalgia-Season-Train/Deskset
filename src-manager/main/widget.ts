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
}

export const activeWidgetMap = reactive(new Map<string, Widget>())
