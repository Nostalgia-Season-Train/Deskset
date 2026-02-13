<script lang="ts" setup>
const widget = defineModel<any>({ required: true })

import desktop from '#manager/global/page/desktop'
const Edit = async (key: string, newValue: any) => {
  await desktop.editWidget(widget.value.id, { [key]: newValue })  // 注意动态键用 [key] 而不用 key
}

import { ElColorPicker } from 'element-plus'
</script>


<template>
<div class="edit-menu">
  <!-- component 不方便调整样式 -->
  <!-- 拆分 v-model，通过父组件自然改变 widget.model -->
  <div class="options" v-for="[key, option] of (Object.entries(widget.options) as any)">
    <!-- *** 颜色选择器 *** -->
    <div class="option" v-if="option.type == 'rgba'">
      <div>{{ option.name }}</div>
      <ElColorPicker show-alpha :model-value="widget.model[key]" @update:model-value="Edit(key, $event)"/>
    </div>
  </div>
</div>
</template>


<style lang="less" scoped>
.option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
