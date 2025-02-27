import { ref } from 'vue'
import { defineStore } from 'pinia'

import { number } from '../../src-components/widget_register'

export const widgetStore = defineStore('status', {
  state: () => ({
    isDisplay: ref(Array(number).fill(false))  // 实际上是组件开关按钮的状态
  })
})


// === 实验性：动态导入 Vue 组件（打包后） ===

// 获取组件信息
const getAllWidgets = async () => {
  const widgets = await window.electron.getAllWidgets()
  console.log(widgets)
}
getAllWidgets()
