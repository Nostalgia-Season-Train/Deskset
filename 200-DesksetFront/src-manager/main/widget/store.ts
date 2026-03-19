import { defineStore } from 'pinia'
import { computed, reactive } from 'vue'
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

  const widgetOnSelect = computed(
    () => activeWidgetOnSelect.value !== null ?
      reactive({
        id: computed(() => activeWidgetOnSelect.value!.id),

        title: computed(() => activeWidgetOnSelect.value!.title),
        name: computed(() => activeWidgetOnSelect.value!.name),
        author: computed(() => activeWidgetOnSelect.value!.author),
        version: computed(() => activeWidgetOnSelect.value!.version),
        descript: computed(() => activeWidgetOnSelect.value!.descript),

        isDragLock: computed({
          get: () => activeWidgetOnSelect.value!.isDragLock,
          set: async (v: boolean) => {
            await desktop.switchWidgetProp(activeWidgetOnSelect.value!.id, 'drag-lock', v)
            activeWidgetOnSelect.value!.isDragLock = v
          }
        }),
        isDisableInteract: computed({
          get: () => activeWidgetOnSelect.value!.isDisableInteract,
          set: async (v: boolean) => {
            await desktop.switchWidgetProp(activeWidgetOnSelect.value!.id, 'disable-interact', v)
            activeWidgetOnSelect.value!.isDisableInteract = v
          }
        }),
        isAutoHide: computed({
          get: () => activeWidgetOnSelect.value!.isAutoHide,
          set: async (v: boolean) => {
            await desktop.switchWidgetProp(activeWidgetOnSelect.value!.id, 'auto-hide', v)
            activeWidgetOnSelect.value!.isAutoHide = v
          }
        })
      }) :
      null
  )
  const selectWidget = async (id: string) => {
    activeWidgetOnSelect.value = activeWidgetMap.get(id) ?? null  // activeWidgetOnSelect.value 指向 activeWidgetMap 实际对象
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
