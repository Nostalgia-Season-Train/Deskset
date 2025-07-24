<script lang="ts" setup>
import desktop from '#manager/global/page/desktop'

const refresh = async () => {
  console.log(await desktop.helloworld())
}
refresh()


/* === SFC 成员 === */
import { ref } from 'vue'
import { Widget } from '#manager/global'

const activeWidgetOnSelect = ref<Widget | null>(null)


/* === SFC 方法 === */
import { getWidgetInfo } from '#manager/main/widget'
import { activeWidgetMap } from '#manager/global'

const appendWidget = async (name: string) => {
  // 生成 ID
  let id = Math.random().toString(16).slice(2)

  for (let n = 0; n < 10; n++) {
    if (!activeWidgetMap.has(id))
      break
    id = Math.random().toString(16).slice(2)
  }

  if (activeWidgetMap.has(id))
    return  // - [ ] 改成 Error

  // 添加部件
  const widgetInfo = await getWidgetInfo(name)

  if (widgetInfo == undefined)
    return  // - [ ] 改成 Error

  const axis = await desktop.appendWidget(id, name)  // 等待桌面添加部件

  activeWidgetMap.set(id, {
    id: id,

    title: name,
    name: name,

    author: widgetInfo.author,
    version: widgetInfo.version,
    descript: widgetInfo.descript,

    isDragLock: false,
    isDisableInteract: false,
    isAutoHide: false,

    x: axis.x,
    y: axis.y
  })
}

const removeWidget = async (id: string) => {
  await desktop.removeWidget(id)
  activeWidgetMap.delete(id)
  activeWidgetOnSelect.value = null
}

const switchWidgetProp = async (id: string, prop: string, state: boolean) => {
  await desktop.switchWidgetProp(id, prop, state)

  // RightInfo 下的 v-model 由本函数切换
  const widget = activeWidgetMap.get(id)

  if (prop == 'drag-lock') widget!.isDragLock = state
  if (prop == 'disable-interact') widget!.isDisableInteract = state
  if (prop == 'auto-hide') widget!.isAutoHide = state
}

const selectActiveWidget = async (id: string) => {
  activeWidgetOnSelect.value = activeWidgetMap.get(id) ?? null
}


/* === Desktop 单向信息 === */
const broadcast = new BroadcastChannel('DesktopSend')

// - [ ] 优化？防抖节流 & 新开线程
broadcast.onmessage = (ev) => {
  const data = ev.data
  const widget = activeWidgetMap.get(data.id)
  widget!.x = data.x
  widget!.y = data.y
}


/* === 子组件 === */
import Menu from './Widget/Left1stMenu.vue'
import List from './Widget/Left2ndList.vue'
import Info from './Widget/RightInfo.vue'
</script>


<template>
<div class="container">

  <div class="left">
    <Menu @select="appendWidget" class="menu"/>
    <List @select="selectActiveWidget" class="list"/>
  </div>

  <div class="right">
    <Info
      v-if="activeWidgetOnSelect"
      v-model="activeWidgetOnSelect"
      class="info"
      @remove="removeWidget"
      @switchProp="switchWidgetProp"
    />
  </div>

</div>
</template>


<style lang="less" scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.container {
  width: 100%;
  height: 100%;
  padding: 0 10px 5px 10px;

  display: flex;
  justify-content: space-between;
  gap: 5px;

  .left {
    width: 25%;
    height: 100%;

    display: flex;
    flex-direction: column;
    gap: 5px;

    :nth-child(2) {
      flex: 1;
    }
  }
  .right {
    width: 75%;
    height: 100%;
  }
}
</style>
