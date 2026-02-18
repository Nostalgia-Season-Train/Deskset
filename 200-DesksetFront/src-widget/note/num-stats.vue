<script lang="ts" setup>
import { ref, watch, toRaw } from 'vue'
import axios from 'axios'

const model = defineModel<{
  /* --- 基础 --- */
  title: string,

  /* --- 筛选 --- */
  filterGroup: any,

  /* --- 样式 --- */
  width: number,
  height: number,
  titleColor: string,
  numberColor: string,
  backgroundColor: string
}>({ required: true })

const number = ref(0)

const refresh = async () => {
  const filterGroup = toRaw(model.value.filterGroup)
  const rep = await axios.post('/v0/note/obsidian/stats/filter-frontmatter', filterGroup)
  number.value = rep.data.result.length
}
refresh()

const openInObsidian = async () => {
  await axios.post('/v0/note/obsidian/stats/filter-and-random-open-in-obsidian', toRaw(model.value.filterGroup))
}

watch(model.value, async () => await refresh())
</script>


<template>
<div
  class="note-stats"
  :style="`width: ${model.width}px; height: ${model.height}px; background: ${model.backgroundColor};`"
  @dblclick="openInObsidian"
>
  <div class="title" :style="`color: ${model.titleColor};`">{{ model.title }}</div>
  <div class="number" :style="`color: ${model.numberColor};`">{{ number }}</div>
</div>
</template>


<style lang="less" scoped>
.note-stats {
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  white-space: nowrap;
  overflow: hidden;

  .title {
    font-size: 20px;
  }
  .number {
    font-size: 36px;
    font-weight: 1000;
  }
}
</style>
