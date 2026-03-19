import { defineStore } from 'pinia'
import { computed } from 'vue'
import desktop from '#manager/main/desktop'
import {
  activeWidgetMap,
  RuntimeWidget,
  activeWidgetOnSelect
} from './mvar'
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

  const widgetOnSelect = activeWidgetOnSelect
  const selectWidget = async (id: string) => {
    activeWidgetOnSelect.value = activeWidgetMap.get(id) ?? null
  }

  const appendWidget = rawAppendWidget
  const removeWidget = async (id: string) => {
    await desktop.removeWidget(id)
    activeWidgetMap.delete(id)
    activeWidgetOnSelect.value = null
  }
  const locateWidget = async (id: string) => {
    await desktop.locateWidget(id)
  }

  return {
    widgets,
    getWidgetNameList,

    widgetOnSelect,
    selectWidget,

    appendWidget,
    removeWidget,
    locateWidget
  }
})
