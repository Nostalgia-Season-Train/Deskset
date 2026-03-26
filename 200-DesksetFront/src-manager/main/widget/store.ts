import { defineStore } from 'pinia'
import { computed, reactive, toRaw, ref, watch } from 'vue'
import { ComputedRef } from 'vue'
import { _t } from '#manager/main/i18n'
import desktop from '#manager/main/desktop'
import { prefixMark } from '#widget/register'
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

  type ComputedRefOf<T> = {
    [K in keyof T]: ComputedRef<T[K]>
  }
  const widgetOnSelect = computed(() => {
    if (activeWidgetOnSelect.value === null)
      return null
    // 编辑部件模型（单个部件实例的配置）
    // 注：在桌面窗口修改 model 时，activeWidgetOnSelect.value!.model 变化会让整个 computed 重新计算，所以不用 watch model
    // 虽然我认为这是个 BUG...
    const tmpModel = ref(structuredClone(toRaw(activeWidgetOnSelect.value!.model)))
    watch(tmpModel.value, async (newModel) => {
      await desktop.editWidget(activeWidgetOnSelect.value!.id, { ...newModel })
      // 验证更改，失败还原当前值。setTimeout 确保在 DesktopSendChannel 响应后执行
      setTimeout(() => tmpModel.value = activeWidgetOnSelect.value!.model)
    })
    return reactive<ComputedRefOf<RuntimeWidget>>({
      id: computed(() => activeWidgetOnSelect.value!.id),

      title: computed({
        get: () => activeWidgetOnSelect.value!.title,
        set: (v: string) => {
          if (v === '') {
            activeWidgetOnSelect.value!.title =
              activeWidgetOnSelect.value!.path.startsWith(prefixMark) ?
                _t(activeWidgetOnSelect.value!.path.replace(prefixMark, '')) : activeWidgetOnSelect.value!.path
          } else {
            activeWidgetOnSelect.value!.title = v
          }
        }
      }),
      path: computed(() => activeWidgetOnSelect.value!.path),
      author: computed(() => activeWidgetOnSelect.value!.author),
      version: computed(() => activeWidgetOnSelect.value!.version),
      descript: computed(() => activeWidgetOnSelect.value!.descript),

      left: computed(() => activeWidgetOnSelect.value!.left),
      top: computed(() => activeWidgetOnSelect.value!.top),
      x: computed({
        get: () => activeWidgetOnSelect.value!.x,
        set: async (v: string) => {
          // 区分 '0' 和 空字符串，空字符串语义代表 null 代表设置默认值
          const x = v !== '' ? Number(v) : null
          const axis = await desktop.setWidgetAxis(activeWidgetOnSelect.value!.id, x, activeWidgetOnSelect.value!.y)
          activeWidgetOnSelect.value!.x = axis.x
          activeWidgetOnSelect.value!.y = axis.y
          // setWidgetAxis 不会触发事件链 drag.ts > DesktopSend > main.ts 更新 widget 位置（left、top）
          activeWidgetOnSelect.value!.left = axis.left
          activeWidgetOnSelect.value!.top = axis.top
        }
      }),
      y: computed({
        get: () => activeWidgetOnSelect.value!.y,
        set: async (v: string) => {
          const y = v !== '' ? Number(v) : null
          const axis = await desktop.setWidgetAxis(activeWidgetOnSelect.value!.id, activeWidgetOnSelect.value!.x, y)
          activeWidgetOnSelect.value!.x = axis.x
          activeWidgetOnSelect.value!.y = axis.y
          activeWidgetOnSelect.value!.left = axis.left
          activeWidgetOnSelect.value!.top = axis.top
        }
      }),
      scale: computed({
        get: () => activeWidgetOnSelect.value!.scale,
        set: async (v: string) => {
          const scale = Number(v) > 0 ? Number(v) : 1
          await desktop.setWidgetScale(activeWidgetOnSelect.value!.id, scale)
          activeWidgetOnSelect.value!.scale = scale
        }
      }),
      opacity: computed({
        get: () => activeWidgetOnSelect.value!.opacity,
        set: async (v: string) => {
          // 透明度可以等于 0
          const opacity = Number(v) >= 0 ? Number(v) : 1
          await desktop.setWidgetOpacity(activeWidgetOnSelect.value!.id, opacity)
          activeWidgetOnSelect.value!.opacity = opacity
        }
      }),

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
      }),

      model: computed(() => tmpModel.value),
      option: computed(() => activeWidgetOnSelect.value!.option)
    })
  })
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
  // - [ ] 主题应用换用此封装
  const clearWidgetList = async () => {
    for (const widget of [...activeWidgetMap.values()]) {
      await desktop.removeWidget(widget.id)
    }
    activeWidgetMap.clear()
    activeWidgetOnSelect.value = null
  }

  return {
    widgets,
    getWidgetNameList,

    widgetOnSelect,
    selectWidget,

    appendWidget,
    removeWidget,
    locateWidget,
    clearWidgetList
  }
})
