import { defineStore } from 'pinia'
import { computed } from 'vue'
import { activeWidgetMap, RuntimeWidget } from './mvar'
import {
  getWidgetNameList as rawGetWidgetNameList,
  appendWidget as rawAppendWidget
} from './mfunc'

export const useWidgetStore = defineStore('widget', () => {
  const widgets = computed({
    get() { return Array.from(activeWidgetMap.values()) as RuntimeWidget[] },
    set() { }
  })
  const getWidgetNameList = rawGetWidgetNameList  // - [ ] 改成属性，监控文件系统更新列表

  const appendWidget = rawAppendWidget

  return { widgets, getWidgetNameList, appendWidget }
})
