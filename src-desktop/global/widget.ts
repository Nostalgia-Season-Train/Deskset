import { reactive, Reactive, WatchHandle } from 'vue'

export interface Widget {
  id: string

  container: HTMLDivElement
  style: HTMLStyleElement | null  // null：内联部件（开发时 Vite 构建打包，而非发布后编译导入）不需要 style 标签
  listens: { event: string, func: any }[]

  // v-model 用作部件配置
  model: Reactive<{ [key: string]: any }>
  unwatch: WatchHandle
}

export const activeWidgetMap = reactive(new Map<string, Widget>())
