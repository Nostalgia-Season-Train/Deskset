<script lang="ts" setup>
import desktop from '#manager/broadcast/desktop'

const refresh = async () => {
  console.log(await desktop.helloworld())
}
refresh()


/* === SFC 成员 === */
import { ref } from 'vue'
import { Widget } from '#manager/main/widget'

const options = ref(Array.from(rawWidgetMap.values()).map(widget => {
  return {
    local: widget.local,
    type: widget.type,
    name: widget.name
  }
}) || [])
const activeWidgetOnSelect = ref<Widget | null>(null)


/* === SFC 方法 === */
import { rawWidgetMap } from '../../src-components/widget'
import { activeWidgetMap } from '#manager/main/widget'

const appendWidget = async (local: string) => {
  // 生成 ID
  let id = Math.random().toString(16).slice(2)

  for (let n = 0; n < 10; n++) {
    if (!rawWidgetMap.has(id))
      break
    id = Math.random().toString(16).slice(2)
  }

  if (rawWidgetMap.has(id))
    return  // - [ ] 改成 Error

  // 添加部件
  const rawWidget = rawWidgetMap.get(local)

  if (rawWidget == undefined)
    return  // - [ ] 改成 Error

  await desktop.appendWidget(id, local)  // 等待桌面添加部件

  activeWidgetMap.set(id, {
    id: id,

    local: local,
    title: rawWidget.name,
    descript: '',

    name: rawWidget.name,
    type: rawWidget.type,

    isDragLock: false,
    isDisableInteract: false,
    isAutoHide: false
  })
}

const selectActiveWidget = async (id: string) => {
  activeWidgetOnSelect.value = activeWidgetMap.get(id) ?? null
}


/* === 子组件 === */
import Menu from './Widget/Left1stMenu.vue'
import List from './Widget/Left2ndList.vue'
import Info from './Widget/RightInfo.vue'
</script>


<template>
<div class="container">

  <div class="left">
    <Menu @select="appendWidget" :options="options" class="menu"/>
    <List @select="selectActiveWidget" class="list"/>
  </div>

  <div class="right">
    <Info v-if="activeWidgetOnSelect" v-model="activeWidgetOnSelect" class="info"/>
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
