<script lang="ts" setup>
const emit = defineEmits(['change'])
type NoteSort = {
  sorts: {
    dataKey: string
    direct: 'asc' | 'desc'  // asc A~Z|0~1，desc Z~A|1~0
  }[]
}
const noteSort = defineModel<NoteSort>({ required: true })

import {
  ElButton,
  ElInput,
  ElSelect
} from 'element-plus'
import { X } from 'lucide-vue-next'
</script>


<template>
<div class="note-sort">
  <ElButton
    @click="noteSort.sorts.push({
      dataKey: 'file.basename',
      direct: 'asc'
    }); emit('change')"
  >添加排序</ElButton>
  <div class="title">
    <div>属性名</div>
    <div>排序方式</div>
    <div>删除</div>
  </div>
  <div class="row" v-for="(sort, index) in noteSort.sorts">
    <ElInput placeholder="Property" v-model="sort.dataKey" @change="emit('change')"/>
    <ElSelect
      :options="[{ value: 'asc', label: '正序' }, { value: 'desc', label: '倒序' }]"
      :props="{ value: 'value', label: 'label' }"
      v-model="sort.direct" @change="emit('change')"
    />
    <ElButton @click="noteSort.sorts.splice(index, 1); emit('change')">
      <X style="width: 16px; height: 16px;"/>
    </ElButton>
  </div>
</div>
</template>


<style lang="less" scoped>
.note-sort {
  .title,
  .row {
    display: flex;
    align-items: center;
    &>:nth-child(1) {
      width: 120px;
    }
    &>:nth-child(2) {
      width: 100px;
    }
    &>:nth-child(3) {
      width: 32px;
    }
  }
}
</style>
