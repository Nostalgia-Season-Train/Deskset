<script lang="ts" setup>
import { RuntimeWidget, RegisterModelOptionItem } from '#manager/global/widget'
const widget = defineModel<
  RuntimeWidget & { option: NonNullable<RuntimeWidget['option']> }  // 传入前父组件已确保 option != undefined
>({ required: true })
const prop = defineProps<{ items: RegisterModelOptionItem[] }>()

import desktop from '#manager/global/page/desktop'
const Edit = async (key: string, newValue: any) => {
  await desktop.editWidget(widget.value.id, { [key]: newValue })  // 注意动态键用 [key] 而不用 key
}

import {
  ElInput,
  ElInputNumber,
  ElColorPicker,
  ElSelect
} from 'element-plus'
import NoteFilter from './EditMenu/NoteFilter.vue'
import NoteProp from './EditMenu/NoteProp.vue'
import NoteSort from './EditMenu/NoteSort.vue'
import NoteGroup from './EditMenu/NoteGroup.vue'
</script>


<template>
<div class="items" v-for="item in prop.items">

  <!-- *** 文本输入框 *** -->
  <div class="item" v-if="item.input == 'Input'">
    <div>{{ item.name }}</div>
    <ElInput
      v-model="widget.model[item.key]"
      @change="Edit(item.key, widget.model[item.key])"
    />
  </div>
  <!-- *** 数字输入框 *** -->
  <div class="item" v-if="item.input == 'InputNumber'">
    <div>{{ item.name }}</div>
    <ElInputNumber
      :controls="false"
      v-model="widget.model[item.key]"
      @change="Edit(item.key, Number(widget.model[item.key]))"
    />
  </div>

  <!-- *** 颜色选择器 *** -->
  <div class="item" v-if="item.input == 'ColorPicker'">
    <div>{{ item.name }}</div>
    <ElColorPicker
      show-alpha
      color-format="hex"
      :clearable="false"
      :model-value="widget.model[item.key]"
      @update:model-value="Edit(item.key, $event)"
    />
  </div>

  <!-- *** 选择器 *** -->
  <div class="item" v-if="item.input == 'Select'">
    <div>{{ item.name }}</div>
    <ElSelect
      :options="(item.parameter as any).choices"
      :props="{ value: 'value', label: 'label' }"
      v-model="widget.model[item.key]"
      @change="Edit(item.key, widget.model[item.key])"
    />
  </div>

  <!-- *** 笔记过滤 *** -->
  <div class="item" v-if="item.input == 'NoteFilter'">
    <NoteFilter
      class="note-filter"
      v-model="widget.model[item.key]"
      @change="Edit(item.key, widget.model[item.key])"
    />
  </div>
  <!-- *** 笔记属性 *** -->
  <div class="item" v-if="item.input == 'NoteProp'">
    <NoteProp
      class="note-prop"
      v-model="widget.model[item.key]"
      @change="Edit(item.key, widget.model[item.key])"
    />
  </div>
  <!-- *** 笔记排序 *** -->
  <div class="item" v-if="item.input == 'NoteSort'">
    <NoteSort
      class="note-sort"
      v-model="widget.model[item.key]"
      @change="Edit(item.key, widget.model[item.key])"
    />
  </div>
  <!-- *** 笔记分组 *** -->
  <div class="item" v-if="item.input == 'NoteGroup'">
    <NoteGroup
      class="note-group"
      v-model="widget.model[item.key]"
      @change="Edit(item.key, widget.model[item.key])"
    />
  </div>

</div>
</template>


<style lang="less" scoped>
.item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .el-input {
    max-width: 50%;
  }
  .el-select {
    max-width: 50%;
  }
  .note-filter {
    width: 100%;
  }
  .note-prop {
    width: 100%;
  }
}
</style>
