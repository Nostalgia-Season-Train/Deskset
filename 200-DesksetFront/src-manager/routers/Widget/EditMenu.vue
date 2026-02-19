<script lang="ts" setup>
import { RuntimeWidget } from '#manager/global/widget'
const widget = defineModel<
  RuntimeWidget & { option: NonNullable<RuntimeWidget['option']> }  // 传入前父组件已确保 option != undefined
>({ required: true })

// 注：没用 component + h 是因为其行为有时很诡异
import EditMenuItem from './EditMenuItem.vue'
import {
  ElScrollbar,
  ElTabs,
  ElTabPane
} from 'element-plus'
</script>


<template>
<div class="edit-menu">
<ElScrollbar max-height="80vh">

  <EditMenuItem v-model="widget" :items="widget.option.items"/>

  <ElTabs class="tab" v-if="widget.option.tabs.length != 0" :default-value="widget.option.tabs[0].id">
    <ElTabPane v-for="tab in widget.option.tabs" :name="tab.id" :label="tab.text">
      <EditMenuItem v-model="widget" :items="tab.items"/>
    </ElTabPane>
  </ElTabs>

</ElScrollbar>
</div>
</template>


<style lang="less" scoped>
.edit-menu {
  width: 100%;

  .tab:has(.note-filter) {
    width: 70vw;
    min-height: 80vh;
  }
}
</style>
