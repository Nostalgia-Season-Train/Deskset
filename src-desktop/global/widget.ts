import { reactive } from 'vue'

export interface Widget {
  id: string

  container: HTMLDivElement
  style: HTMLStyleElement
  listens: { event: string, func: any }[]
}

export const activeWidgetMap = reactive(new Map<string, Widget>())
