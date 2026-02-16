<script lang="ts" setup>
import { RuntimeWidget } from '#manager/global/widget'
const widget = defineModel<
  RuntimeWidget & { option: NonNullable<RuntimeWidget['option']> }  // 传入前父组件已确保 option != undefined
>({ required: true })

import desktop from '#manager/global/page/desktop'
const Edit = async (key: string, newValue: any) => {
  await desktop.editWidget(widget.value.id, { [key]: newValue })  // 注意动态键用 [key] 而不用 key
}

import NoteFilter from './EditMenu/NoteFilter.vue'
import NoteProp from './EditMenu/NoteProp.vue'
import {
  ElScrollbar,
  ElTabs,
  ElTabPane,
  ElInput,
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

  <ElTabs class="tab" v-if="widget.option.tabs.length != 0" :default-value="widget.option.tabs[0].id">
    <ElTabPane v-for="tab in widget.option.tabs" :name="tab.id" :label="tab.text">
      <div class="items" v-for="item in tab.items">
        <!-- *** 文本输入框 *** -->
        <div class="item" v-if="item.input == 'str'">
          <div>{{ item.name }}</div>
          <ElInput v-model="widget.model[item.key]" @change="Edit(item.key, widget.model[item.key])"/>
        </div>
        <!-- *** 数字输入框 *** -->
        <div class="item" v-if="item.input == 'num'">
          <div>{{ item.name }}</div>
          <ElInput v-model="widget.model[item.key]" @change="Edit(item.key, Number(widget.model[item.key]))"/>
        </div>
        <!-- *** 颜色选择器 *** -->
        <div class="item" v-if="item.input == 'rgba'">
          <div>{{ item.name }}</div>
          <ElColorPicker show-alpha :model-value="widget.model[item.key]" @update:model-value="Edit(item.key, $event)"/>
        </div>
        <!-- *** 笔记过滤 *** -->
        <div class="item" v-if="item.input == 'noteFilter'">
          <NoteFilter class="note-filter" v-model="widget.model[item.key]" @change="Edit(item.key, widget.model[item.key])"/>
        </div>
        <!-- *** 笔记属性 *** -->
        <div class="item" v-if="item.input == 'noteProp'">
          <NoteProp class="note-prop" v-model="widget.model[item.key]" @change="Edit(item.key, widget.model[item.key])"/>
        </div>
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
    &>.el-input {
      max-width: 50%;
    }
  }
  .tab:has(.note-filter) {
    width: 70vw;
    min-height: 80vh;
  }
  .note-filter {
    width: 100%;
  }
  .note-prop {
    width: 100%;
  }
}
</style>
