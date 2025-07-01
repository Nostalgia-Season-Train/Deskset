import { reactive } from 'vue'

export interface Widget {
  id: string

  container: HTMLElement
  listens: { event: string, func: any }[]
}

export const activeWidgetMap = reactive(new Map<string, Widget>())
