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
import { ref } from 'vue'

const isOpenDialog = ref(false)
const dialogTitle = ref<string>('')
const dialogOptions = ref<{ name: string, type: string }[]>([])

const editWidget = async (id: string) => {
  const widget = activeWidgetMap.get(id)
  if (widget!.options == null)
    return
  dialogTitle.value = `编辑 ${widget!.title} 配置`
  dialogOptions.value = widget!.options
  isOpenDialog.value = true
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '#shadcn/components/ui/dialog'
import { ElColorPicker } from 'element-plus'
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
      @edit="editWidget"
      @switchProp="switchWidgetProp"
    />
  </div>

  <!-- @openAutoFocus.prevent：禁用自动聚焦 -->
  <!-- :modal=false：让 Element Plus 选择器能被点击 -->
  <!-- @interact-outside.prevent：让 Element Plus 选择器确认后，DialogContent 不会直接关闭 -->
  <Dialog v-model:open="isOpenDialog" :modal="false">
    <DialogContent @openAutoFocus.prevent @interact-outside.prevent>
      <DialogHeader>
        <DialogTitle>{{ dialogTitle }}</DialogTitle>
        <DialogDescription></DialogDescription>
      </DialogHeader>
      <div
        class="flex justify-between items-center"
        v-for="option in dialogOptions"
      >
        <div>{{ option.name }}</div>
        <component v-if="option.type == 'ColorPicker'" :is="ElColorPicker"/>
      </div>
    </DialogContent>
  </Dialog>

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
