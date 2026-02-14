<script lang="ts" setup>
import { RuntimeWidget } from '#manager/global/widget'
const widget = defineModel<
  RuntimeWidget & { option: NonNullable<RuntimeWidget['option']> }  // 传入前父组件已确保 option != undefined
>({ required: true })

import desktop from '#manager/global/page/desktop'
const Edit = async (key: string, newValue: any) => {
  await desktop.editWidget(widget.value.id, { [key]: newValue })  // 注意动态键用 [key] 而不用 key
}

import {
  ElScrollbar,
  ElTabs,
  ElTabPane,
  ElColorPicker
} from 'element-plus'
</script>


<template>
<div class="edit-menu">
<ElScrollbar max-height="80vh">

  <!-- component 不方便调整样式 -->
  <!-- 拆分 v-model，通过父组件自然改变 widget.model -->
  <div class="items" v-for="item in widget.option.items">
    <!-- *** 颜色选择器 *** -->
    <div class="item" v-if="item.input == 'rgba'">
      <div>{{ item.name }}</div>
      <ElColorPicker show-alpha :model-value="widget.model[item.key]" @update:model-value="Edit(item.key, $event)"/>
    </div>
  </div>

  <ElTabs v-if="widget.option.tabs.length != 0" :default-value="widget.option.tabs[0].id">
    <ElTabPane v-for="tab in widget.option.tabs" :name="tab.id" :label="tab.text">
      <div class="items" v-for="item in tab.items">
        <div class="item">{{ item }}</div><!-- [ ] 逻辑优化后，再完成该功能 -->
      </div>
    </ElTabPane>
  </ElTabs>

</ElScrollbar>
</div>
</template>


<style lang="less" scoped>
.edit-menu {
  width: 100%;

  .item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
