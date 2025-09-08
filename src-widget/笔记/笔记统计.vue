<script lang="ts" setup>
import { ref, watch, toRaw } from 'vue'
import axios from 'axios'

const model = defineModel<{
  title: string,
  filterGroup: any
}>({ required: true })

const number = ref(0)

const refresh = async () => {
  const filterGroup = toRaw(model.value.filterGroup)
  const rep = await axios.post('/v0/note/obsidian/stats/filter-frontmatter-number', filterGroup)
  number.value = rep.data.result
}
refresh()

const openInObsidian = async () => {
  await axios.post('/v0/note/obsidian/stats/filter-and-random-open-in-obsidian', toRaw(model.value.filterGroup))
}

watch(model.value, async () => await refresh())
</script>


<template>
<div class="note-stats" @dblclick="openInObsidian">
  <div class="title">{{ model.title }}</div>
  <div class="number">{{ number }}</div>
</div>
</template>


<style lang="less" scoped>
.note-stats {
  width: 244px;  // 全宽 270 = 244 + 12*2 + 1*2
  height: 82px;  // 全高 100 = 82 + 8*2 + 1*2
  padding: 8px 12px;
  background: #FFF7;
  border: solid 1px #FFF;

  .title {
    color: #000;
    font-size: 24px;
  }
  .number {
    color: #000D;
    font-size: 40px;
    font-weight: 1000;
  }
}
</style>
