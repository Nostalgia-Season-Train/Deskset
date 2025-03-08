<script setup>
/* === 组件 === */
import { shallowRef, triggerRef } from 'vue'
import { defineAsyncComponent } from 'vue'
import { widgets as rawWidgets } from '../src-components/widget_register'

const widgets = shallowRef(rawWidgets)

// 设置组件
// 注：仅当应用主题时使用 widgetStyle，因为拖动指令是直接操作 DOM，没有响应式绑定
const setWidget = async ({widgetId, isDisplay=undefined, widgetClass=undefined, widgetStyle=undefined, widgetModel=new Object}) => {
  const num = widgets.value.findIndex(widget => widget.id == widgetId)
  if (num == -1) {
    throw Error(`没有 ${widgetId} 组件`)
  }

  if (isDisplay == true) {
    // 打开组件
    widgets.value[num].isDisplay = true

    // 异步加载组件（注：widgets.value[num].content 也会改变 rawWidgets[num].content）
    widgets.value[num].contentLoad = defineAsyncComponent(widgets.value[num].content)
    if (widgetClass != undefined) {  // 传入 array，:class="['prop']" = :class="prop"
      widgets.value[num].class = widgetClass
    }
    widgets.value[num].style = widgetStyle
    widgets.value[num].model = widgetModel  // 父组件和子组件间，通过 v-model 双向绑定数据
  } else if (isDisplay == false) {
    // 关闭组件，并清空组件状态
    widgets.value[num].isDisplay = false

    widgets.value[num].contentLoad = undefined
    widgets.value[num].class = undefined
    widgets.value[num].style = undefined
    widgets.value[num].model = undefined
  }

  // shallowRef.value.arry 不是响应式的，手动更新
  triggerRef(widgets)

  // 返回 Promise 确保 switchWidgetDisplay 能被正确 await
  return new Promise((resolve) => { resolve() })  // 中括号包裹函数保持行为一致
}

// 切换组件属性（仅限打开的组件）
const switchWidgetProp = async (id, prop, is) => {
  const num = widgets.value.findIndex(widget => widget.id == id)
  if (num == -1) {
    throw Error(`没有 ${id} 组件`)
  }

  // is = true 添加 prop；is = false 移除 prop
  if (widgets.value[num].isDisplay == true) {
    let widgetProps = new Set(widgets.value[num].class)

    if (is == true) {
      widgetProps.add(prop)
    } else {
      widgetProps.delete(prop)
    }

    widgets.value[num].class = Array.from(widgetProps)
  }

  triggerRef(widgets)
}

// 关闭所有组件，await Promise.all() 等待异步全部完成
const closeAllWidgets = async () => {
  await Promise.all(widgets.value.map((widget) => setWidget({widgetId: widget.id, isDisplay: false})))
}


/* === 主题 === */

// 保存主题
import dayjs from "dayjs"

const saveTheme = async (themeName) => {
  let themeData = {}

  // 保存日期
  themeData['savetime'] = String(dayjs().format('YYYY-MM-DD HH:mm:ss'))

  // 组件状态
  let widgetStatus = []

  for (const widget of widgets.value) {
    const widgetHTML = document.getElementById(widget.id)
    if (widgetHTML != null) {
      widgetStatus.push({
        id: widget.id,
        class: Array.from(widgetHTML.classList),  // class 标注属性，方便改变组件行为
        style: widgetHTML.style.cssText,  // 拖拽不会改变 widget.style
        model: widget.model
      })
    }
  }

  themeData['widgets'] = widgetStatus

  // 发送主题数据
  const theme = {
    name: themeName,
    widget: themeData
  }

  window.winDesktop.saveTheme(theme)
}

// 使用主题
const useTheme = async (themeName) => {
  const theme = await window.winDesktop.getOneTheme(themeName)
  if (theme == undefined) {
    throw Error(`主题 ${themeName} 读取失败`)
  }

  const widgets = theme?.data?.widgets
  if (widgets == undefined) {
    throw Error(`主题 ${themeName} 中的组件读取失败`)
  }

  // 先关闭当前组件，再打开
  await closeAllWidgets()
  for (const widget of widgets) {
    const widgetId = widget?.id
    if (widgetId != undefined) {
      await setWidget({widgetId: widgetId, isDisplay: true, widgetClass: widget?.class, widgetStyle: widget?.style, widgetModel: widget?.model})
    }
  }

  // 应用 css 样式

  // 清除上次样式
  const lastStyle = document.querySelector('link[deskset="themeStyle"]')
  if (lastStyle != undefined) {
    lastStyle.remove()
  }

  // 当主题文件夹存在 .css 样式文件时，应用样式
  const style = theme?.style
  if (style != undefined) {
    const linkStyle = document.createElement('link')
    linkStyle.setAttribute('deskset', 'themeStyle')
    linkStyle.rel = 'stylesheet'
    linkStyle.href = style

    document.head.appendChild(linkStyle)  // 附：打包后，样式更改不会实时生效
  }
}


/* === 开发 === */

// 刷新桌面
const refreshPage = async () => {
  location.reload()
}


/* === 管理页控制桌面页 === */

// 桌面管理：跨页面通信，管理页 /manager.html
const bc = new BroadcastChannel("pageDesktop")
const pageManager = new BroadcastChannel('pageManager')

bc.onmessage = async (event) => {
  /* === 组件 === */
  if (event.data?.action == 'getWidgetOnDesktop') {
    const widgetId = event.data?.id
    const widgetHTML = document.getElementById(widgetId)
    if (widgetHTML != null) {
      const widget = {
        'id': widgetId,
        'isDisplay': true,
        'class': Array.from(widgetHTML.classList),
        'style': widgetHTML.style.cssText
      }
      pageManager.postMessage(widget)
    } else {
      const widget = {
        'id': widgetId,
        'isDisplay': false,
        'class': [],
        'style': ''
      }
      pageManager.postMessage(widget)
    }
  } else if (event.data?.action == 'switchDisplay') {
    // 切换组件显示
    const id = event.data.id
    const isDisplay = event.data.isDisplay

    setWidget({widgetId: id, isDisplay: isDisplay})
  } else if (event.data?.action == 'switchProp') {
    // 切换组件属性
    switchWidgetProp(event.data.id, event.data.prop, event.data.is)
  }

  /* === 主题 === */
  if (event.data?.action == "saveTheme") {
    saveTheme(event.data?.themeName)
  }
  if (event.data?.action == "useTheme") {
    useTheme(event.data?.themeName)
  }

  /* === 开发 === */
  if (event.data?.action == "refreshPage") {
    refreshPage()
  }
}
</script>


<template>
<body>
  <!-- 组件容器 -->
  <div class="container">
    <div v-for="widget in widgets">
      <Suspense>
        <div
          :id="widget.id"
          :class="widget.class"
          :style="widget.style"
          v-if="widget.isDisplay"
          v-widget-drag
        >
          <component :is="widget.contentLoad" v-model="widget.model"/>
        </div>
      </Suspense>
    </div>
  </div>
</body>
</template>


<style scoped>
* {
  box-sizing: border-box;
  margin: 0; padding: 0;

  user-select: none;
}

body {
  width: 100vw; height: 100vh;

  background-color: transparent;

  display: flex; flex-direction: row;
}

.container {
  min-width: 100vw; min-height: 100vh;

  display: flex; flex-direction: column;
  align-items: center;
}

/* 禁用交互，除了包裹组件的 div */
.disable-interaction * {
  /* ' *' 是最优解，对于绑定在 body 上的 el-date-picker 也起作用 */
  pointer-events: none;
}

/* 自动隐藏，鼠标移入时显示 */
.auto-hide {
  background-color: #FFFFFF01;
}
.auto-hide>* {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}
.auto-hide:hover>* {
  opacity: 1;
  visibility: visible;
}
</style>
