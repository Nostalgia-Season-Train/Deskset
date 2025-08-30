<script lang="ts" setup>
const emit = defineEmits(['change'])

type Filter = {
  type: string
  isInvert: boolean
  frontmatterKey: string
  compareValue: string
}
type FilterArray = Array<Filter | FilterArray>

const filters = defineModel<FilterArray>({ required: true })

import {
  ElButton,
  ElInput,
  ElSwitch,
  ElSelect,
  ElOption
} from 'element-plus'
import { X } from 'lucide-vue-next'
</script>


<template>
<div>
  <!-- 添加按钮 -->
  <ElButton
    style="padding: 0 6px;"
    @click="filters.push({
      type: 'is',
      isInvert: false,
      frontmatterKey: '',
      compareValue: ''
    }); emit('change')"
  >添加条件</ElButton>
  <ElButton
    style="margin: 0; padding: 0 6px;"
    @click="filters.push([{
      type: 'is',
      isInvert: false,
      frontmatterKey: '',
      compareValue: ''
    }]); emit('change')"
  >添加条件组</ElButton>
  <div class="flex">
    <span style="width: 120px;">属性名</span>
    <span style="width: 40px;">取反</span>
    <span style="width: 120px">条件</span>
    <span class="flex-1">比较值</span>
    <span>删除</span>
  </div>
  <!-- 过滤器 -->
  <div v-for="(filter, index) in filters">
    <div v-if="!Array.isArray(filter)" class="flex">
      <ElInput
        style="width: 120px;"
        v-model="filter.frontmatterKey"
        placeholder="Frontmatter"
        @change="emit('change')"
      />
      <ElSwitch
        style="width: 40px;"
        v-model="filter.isInvert"
        @change="emit('change')"
      />
      <ElSelect v-model="filter.type" @change="emit('change')" style="width: 120px">
        <ElOption value="is" style="padding: 0 12px;"/>
        <ElOption value="startsWith" style="padding: 0 12px;"/>
        <ElOption value="endsWith" style="padding: 0 12px;"/>
        <ElOption value="isEmpty" style="padding: 0 12px;"/>
        <ElOption value="contains" style="padding: 0 12px;"/>
      </ElSelect>
      <ElInput
        class="flex-1"
        style="width: 0;"
        v-model="filter.compareValue"
        placeholder="Value"
        :disabled="filter.type == 'isEmpty'"
        @change="emit('change')"
      /><!-- width: 0; 抵消默认宽度 -->
      <ElButton
        style="width: 30px;"
        @click="
          filters.splice(index, 1);
          emit('change')
        "
      >
        <X style="width: 16px; height: 16px;"/>
      </ElButton>
    </div>
    <div v-else class="ml-1 border border-gray-300">
      <OptionFilter
        v-model="filters[index] as any[]"
        @change="() => {
          if ((filters[index] as any[]).length == 0)
            filters.splice(index, 1)
          emit('change')
        }"
      />
    </div>
  </div>
</div>
</template>
