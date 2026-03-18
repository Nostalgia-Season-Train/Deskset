import { defineStore } from 'pinia'
import { computed } from 'vue'
import { activeWidgetMap, RuntimeWidget } from './mvar'

export const useWidgetStore = defineStore('widget', () => {
  const widgets = computed({
    get() { return Array.from(activeWidgetMap.values()) as RuntimeWidget[] },
    set() { }
  })

  return { widgets }
})
