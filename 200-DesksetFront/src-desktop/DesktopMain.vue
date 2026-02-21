<script lang="ts" setup>
const helloworld = async () => {
  return 'helloworld'
}


/* === 全局变量&函数 === */
import { activeWidgetMap } from './global/widget'
import { compileCache } from './global/cache'
import dragAndDrop from './drag'


/* === SFC 成员 === */
import { useTemplateRef } from 'vue'

const desktopMain = useTemplateRef('desktopMain')


/* === SFC 方法 === */
import { h, render, defineAsyncComponent } from 'vue'
import { reactive, watch, toRaw } from 'vue'
import { compile } from './main/compile'
import { inlineRawWidgetMap, prefixMark } from '#widget/register'
import { stat, BaseDirectory } from '@tauri-apps/plugin-fs'
import { DesktopSendChannel } from './global/channel'

const desktopSend = DesktopSendChannel

const appendWidget = async (
  id: string,
  name: string,
  isDragLock: boolean | null,
  isDisableInteract: boolean | null,
  isAutoHide: boolean | null,
  left: number | null,
  top: number | null,
  scale: number | null,
  model: Record<string, any>
) => {
  let component
  let style

  if (name.startsWith(prefixMark)) {
    component = defineAsyncComponent(inlineRawWidgetMap.get(name)!.main)
    style = null
  } else {
    // 查找编译缓存
    const mtime = (await stat(`./widgets/${name}/main.vue`, { baseDir: BaseDirectory.Resource })).mtime?.toString() ?? null

    let cache = compileCache.get(name)
    if (cache == undefined || cache.mtime != mtime) {
      const code = await compile(name)
      compileCache.set(name, {
        mtime: mtime,
        jsModule: URL.createObjectURL(new Blob([code.js], { type: 'text/javascript' })),
        cssCode: code.css
      })
    }
    cache = compileCache.get(name)

    // 导入 JS 代码
    component = defineAsyncComponent(() => import(/* @vite-ignore */cache!.jsModule))

    // 导入 CSS 代码
      // - [ ] 后续使用编译缓存管理
    style = Object.assign(document.createElement('style'), {
      textContent: cache!.cssCode,
      type: 'text/css'
    })
    document.head.appendChild(style)
  }

  // 0、挂载等待
  let mountSignal: Function
  const mountWait = new Promise<void>((resolve) => mountSignal = () => resolve())

  // 1、渲染组件
  const vnode = h(component, {
    onVnodeMounted: () => mountSignal(),
    // 组件 v-model：虽然不规范，但是这里只能用 reactive
      // 使用常量：model 无法修改
      // 使用 ref：嵌套两个 value
    modelValue: reactive(model)
  })
  const container = document.createElement('div')
  container.id = id  // 用于原生 js 根据 id 获取部件所在 div
  container.style.position = 'absolute'
  container.style.left = '0px'
  container.style.top = '0px'
  container.style.transformOrigin = 'center center'  // 以 container 中心作变换；适用于缩放
  render(vnode, container)
  // if (url != null) {
  //   URL.revokeObjectURL(url)  // NodeJS 和浏览器均不能析构 import() 缓存
  // }

  // 2、添加监听器
  const drag = dragAndDrop(container)
  container.addEventListener('mousedown', drag)

  // 3、附着组件
  desktopMain.value!.appendChild(container)

  // 4、居中组件
  await mountWait
  container.style.left = desktopMain.value!.offsetWidth / 2 - container.offsetWidth / 2 + 'px'
  container.style.top = desktopMain.value!.offsetHeight / 2 - container.offsetHeight / 2 + 'px'

  // 5、初始化时，直接设置组件属性、位置
  const finalIsDragLock = isDragLock != null ? isDragLock : false
  const finalIsDisableInteract = isDisableInteract != null ? isDisableInteract : false
  const finalIsAutoHide = isAutoHide != null ? isAutoHide : false

  container.classList.toggle('deskset_drag-lock', finalIsDragLock)
  container.classList.toggle('deskset_disable-interact', finalIsDisableInteract)
  container.classList.toggle('deskset_auto-hide', finalIsAutoHide)

  if (left != null) container.style.left = left + 'px'
  if (top != null) container.style.top = top + 'px'

  const finalScale = scale != null ? scale : 1
  container.style.transform = `scale(${finalScale})`

  // 6、监听组件 v-model 变化
  const unwatch = watch(
    vnode.props!.modelValue,
    async () => desktopSend.postMessage({
      id: id,
      model: toRaw(vnode.props!.modelValue)
    })
  )

  activeWidgetMap.set(id, {
    id: id,
    container: container,
    style: style,
    listens: [
      { event: 'mousedown', func: drag }
    ],
    model: vnode.props!.modelValue,
    unwatch: unwatch
  })

  return {
    isDragLock: finalIsDragLock,
    isDisableInteract: finalIsDisableInteract,
    isAutoHide: finalIsAutoHide,
    x: (container.offsetLeft + (container.offsetWidth >> 1)) * window.devicePixelRatio | 0,
    y: (container.offsetTop + (container.offsetHeight >> 1)) * window.devicePixelRatio | 0,
    left: container.offsetLeft,
    top: container.offsetTop,
    scale: finalScale,
    model: vnode.props!.modelValue
  }
}

/* --- 删除部件 --- */
const removeWidget = async (id: string) => {
  const widget = activeWidgetMap.get(id)

  widget!.unwatch()
  for (const listen of widget!.listens) {
    widget!.container.removeEventListener(listen.event, listen.func)
  }
  render(null, widget!.container)
  desktopMain.value!.removeChild(widget!.container)
  if (widget!.style != null) {
    document.head.removeChild(widget!.style)
  }

  activeWidgetMap.delete(id)
}

/* --- 编辑部件 --- */
const editWidget = async (id: string, model: Record<string, any>) => {
  const widget = activeWidgetMap.get(id)

  Object.assign(widget!.model, model)
}

/* --- 定位部件 --- */
const locateWidget = async (id: string) => {
  if (activeWidgetMap.get(id)!.container.classList.contains('deskset_locate'))  // 确保上一个定时器已经清除 deskset_locate
    return
  activeWidgetMap.get(id)!.container.classList.toggle('deskset_locate', true)

  setTimeout(async () => {
    const container = activeWidgetMap.get(id)?.container
    if (container != undefined)  // 检查部件是否删除
      container.classList.toggle('deskset_locate', false)
  }, 3 * 1000)
}

/* --- 设置部件位置 --- */
const setWidgetAxis = async (id: string, x: number | null, y: number | null) => {
  const widget = activeWidgetMap.get(id)

  const container = widget!.container

  const dpr = window.devicePixelRatio
  const width = container.offsetWidth
  const height = container.offsetHeight

  const left = x ? (x / dpr) - (width >> 1) : desktopMain.value!.offsetWidth / 2 - width / 2
  const top = y ? (y / dpr) - (height >> 1) : desktopMain.value!.offsetHeight / 2 - height / 2
  container.style.left = left + 'px'
  container.style.top = top + 'px'

  // 计算并传出最终 x, y，方便检查是否跟传入最初 x, y 一致
  return {
    x: (container.offsetLeft + (container.offsetWidth >> 1)) * window.devicePixelRatio | 0,
    y: (container.offsetTop + (container.offsetHeight >> 1)) * window.devicePixelRatio | 0,
    left: left,
    top: top
  }
}

/* --- 设置部件大小 --- */
const setWidgetScale = async (id: string, scale: number) => {
  const widget = activeWidgetMap.get(id)

  const container = widget!.container
  container.style.transform = `scale(${scale})`
}

/* --- 切换部件属性 --- */
const switchWidgetProp = async (id: string, prop: string, state: boolean) => {
  const widget = activeWidgetMap.get(id)

  widget!.container.classList.toggle('deskset_' + prop, state)
}

const getWindowData = async () => {
  return {
    width: window.innerWidth,
    height: window.innerHeight,
    dpr: window.devicePixelRatio
  }
}


/* ==== BroadcastDesktopServer ==== */
  // 将 Broadcast 由事件/消息改成请求/响应模型
import { onMounted, onUnmounted } from 'vue'
import { DesktopChannel } from './global/channel'

const actions = {
  helloworld,

  appendWidget,
  removeWidget,
  editWidget,
  locateWidget,

  setWidgetAxis,
  setWidgetScale,
  switchWidgetProp,

  getWindowData
}
const broadcast = DesktopChannel
const onReceive = async (msg: MessageEvent) => {
  const request = JSON.parse(msg.data)

  let result, error
  try {
    result = await (actions as any)[request.funcName](...request.funcArgs)
  } catch (err) {
    if (err instanceof Error) {
      error = {
        name: err.name,
        message: err.message,
        stack: err?.stack
      }
    } else {
      error = {
        name: 'unknown error',
        message: 'unknown error type',
        stack: undefined
      }
    }
  }

  broadcast.postMessage(
    JSON.stringify({
      id: request.id,
      result: result,
      error: error
    })
  )
}

onMounted(() => broadcast.onmessage = onReceive)
onUnmounted(() => broadcast.onmessage = null)
</script>



<template>
<div id="desktopMain" ref="desktopMain"></div>
</template>



<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  user-select: none;
}

#desktopMain {
  /* 避免部件移动到桌面外造成的桌面 div 移位 */
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;

  width: 100vw;
  height: 100vh;
}
</style>

<style>
/* --- 定位部件 --- */
.deskset_locate {
  outline: 3px solid Red;
}

/* --- 禁用交互 --- */
  /* 注：* 使子元素也禁用交互 */
.deskset_disable-interact * {
  pointer-events: none;
}

/* --- 自动隐藏 --- */
.deskset_auto-hide>* {
  opacity: 0;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}
.deskset_auto-hide:hover>* {
  opacity: 1;
}
</style>
