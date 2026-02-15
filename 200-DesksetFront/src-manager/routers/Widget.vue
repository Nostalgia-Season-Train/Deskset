<script lang="ts" setup>
import desktop from '#manager/global/page/desktop'

const refresh = async () => {
  console.log(await desktop.helloworld())
}
refresh()


/* === SFC 成员 === */
import {
  activeWidgetMap,
  activeWidgetOnSelect
} from '#manager/global'


/* === SFC 方法 === */
import { appendWidget } from '#manager/main/widget'

const removeWidget = async (id: string) => {
  await desktop.removeWidget(id)
  activeWidgetMap.delete(id)
  activeWidgetOnSelect.value = null
}

/* --- 编辑部件配置 --- */
import { h } from 'vue'
import { ElMessageBox } from 'element-plus'
import Edit from './Widget/EditMenu.vue'

const editWidget = async (id: string) => {
  const widget = activeWidgetMap.get(id)
  // 交给编辑按钮判断即可，这样不用改两处
  // if (widget!.option == undefined)
  //   return
  ElMessageBox({
    title: `编辑 ${widget!.title} 配置`,
    showConfirmButton: false,
    message: () => h(Edit, { modelValue: widget as any }),  // 编辑按钮已判断 option != undefined
    callback: () => {}
  })
}

const locateWidget = async (id: string) => {
  await desktop.locateWidget(id)
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


/* === 子组件 === */
import Menu from './Widget/Left1stMenu.vue'
import List from './Widget/Left2ndList.vue'
import Info from './Widget/RightInfo.vue'
</script>


<template>
<div class="container-widget">

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
      @edit="editWidget"
      @locate="locateWidget"
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

/* --- Transition --- */
.v-enter-active,
.v-leave-active {
  transition: opacity .15s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}

/* --- Element Plus --- */
:deep(.el-input) {
  width: 185px;  // 缩小输入框宽度，让选择器在左侧显示
}

.container-widget {
  width: 100%;
  height: 100%;
  padding: var(--content-padding);
  padding-top: 0;

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
