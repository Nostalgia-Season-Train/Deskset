<script lang="ts" setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const model = defineModel<{
  title: string,
  filters: any[]
}>({ required: true })

const number = ref(0)

const refresh = async () => {
  const rep = await axios.post('/v0/note/obsidian/stats/filter-frontmatter-number', model.value.filters)
  number.value = rep.data.result
}
refresh()

watch(model.value, async () => await refresh())
</script>


<template>
<div class="note-stats">
  <div class="title">{{ model.title }}</div>
  <div class="number">{{ number }}</div>
</div>
</template>


<style lang="less" scoped>
.note-stats {
  width: 240px;
  height: 80px;
  padding: 8px 12px;
  color: #000;
  background: #FFF7;
  border: solid 1px #FFF;

  .title {
    font-size: 24px;
  }
  .number {
    font-size: 40px;
    font-weight: 1000;
  }
}
</style>
