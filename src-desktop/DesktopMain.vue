<script lang="ts" setup>
const helloworld = async () => {
  return 'helloworld'
}


/* === 全局变量&函数 === */
import { rawWidgetMap } from '../src-widget/widget'
import { activeWidgetMap } from './main/widget'
import dragAndDrop from './drag'


/* === SFC 成员 === */
import { useTemplateRef } from 'vue'

const desktopMain = useTemplateRef('desktopMain')


/* === SFC 方法 === */
import { h, render, defineAsyncComponent } from 'vue'

const appendWidget = async (id: string, local: string) => {
  const component = defineAsyncComponent(rawWidgetMap.get(local)!.content)

  // 0、挂载等待
  let mountSignal: Function
  const mountWait = new Promise<void>((resolve) => mountSignal = () => resolve())

  // 1、渲染组件
  const vnode = h(component, {
    onVnodeMounted: () => mountSignal()
  })
  const container = document.createElement('div')
  container.id = id  // 用于原生 js 根据 id 获取部件所在 div
  container.style.position = 'absolute'
  container.style.left = '0px'
  container.style.top = '0px'
  render(vnode, container)

  // 2、添加监听器
  const drag = dragAndDrop(container)
  container.addEventListener('mousedown', drag)

  // 3、附着组件
  desktopMain.value!.appendChild(container)

  // 4、居中组件
  await mountWait
  container.style.left = desktopMain.value!.offsetWidth / 2 - container.offsetWidth / 2 + 'px'
  container.style.top = desktopMain.value!.offsetHeight / 2 - container.offsetHeight / 2 + 'px'

  activeWidgetMap.set(id, {
    id: id,
    container: container,
    listens: [
      { event: 'mousedown', func: drag }
    ]
  })

  return { x: container.offsetLeft + (container.offsetWidth >> 1), y: container.offsetTop + (container.offsetHeight >> 1) }
}

const removeWidget = async (id: string) => {
  const widget = activeWidgetMap.get(id)

  for (const listen of widget!.listens) {
    widget!.container.removeEventListener(listen.event, listen.func)
  }
  render(null, widget!.container)
  desktopMain.value!.removeChild(widget!.container)

  activeWidgetMap.delete(id)
}

const switchWidgetProp = async (id: string, prop: string, state: boolean) => {
  const widget = activeWidgetMap.get(id)

  widget!.container.classList.toggle('deskset_' + prop, state)
}


/* ==== BroadcastDesktopServer ==== */
  // 将 Broadcast 由事件/消息改成请求/响应模型
import { onMounted, onUnmounted } from 'vue'

const actions = {
  helloworld,
  appendWidget,
  removeWidget,
  switchWidgetProp
}
const broadcast = new BroadcastChannel('Desktop')
const onReceive = async (msg: MessageEvent) => {
  const request = JSON.parse(msg.data)

  let result, error
  try {
    result = await (actions as any)[request.funcName](...request.funcArgs)
  } catch (err) {
    error = err
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
