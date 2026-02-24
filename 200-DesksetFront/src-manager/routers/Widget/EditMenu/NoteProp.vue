<script lang="ts" setup>
const emit = defineEmits(['change'])

type NoteProp = {
  props: {
    dataKey: string
    title: string
    width: number
  }[]
}

const noteProp = defineModel<NoteProp>({ required: true })

import {
  ElButton,
  ElInput
} from 'element-plus'
import { X } from 'lucide-vue-next'
</script>


<template>
<div>
  <ElButton
    style="padding: 0 6px;"
    @click="noteProp.props.push({
      dataKey: 'file.basename',
      title: '文件主名',
      width: 300
    }); emit('change')"
  >添加属性</ElButton>
  <div style="display: flex;">
    <div style="width: 120px;">属性名</div>
    <div style="flex: 1;">标题</div>
    <div style="width: 80px;">宽度</div>
    <div>删除</div>
  </div>
  <div v-for="(prop, index) in noteProp.props" style="display: flex;">
    <ElInput
      style="width: 120px;"
      v-model="prop.dataKey"
      placeholder="Property"
      @change="emit('change')"
    />
    <ElInput
      style="width: 0; flex: 1;"
      v-model="prop.title"
      placeholder="Title"
      @change="emit('change')"
    />
    <ElInput
      style="width: 80px;"
      v-model="prop.width"
      placeholder="Width"
      @change="
        prop.width = Number(prop.width);
        emit('change')
      "
    />
    <ElButton
      style="width: 30px;"
      @click="
        noteProp.props.splice(index, 1);
        emit('change')
      "
    >
      <X style="width: 16px; height: 16px;"/>
    </ElButton>
  </div>
</div>
</template>
