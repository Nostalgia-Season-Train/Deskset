<script setup>
import { ref } from 'vue'
import { desksetReq } from '../request'

const recentOpenList = ref([])

const refresh = async () => {
  const rep = await desksetReq.get('/v0/obsidian/recent/recent-open')
  recentOpenList.value = rep.data.data
}
refresh()

const open = async (relpath) => {
  desksetReq.get(`/v0/obsidian/manager/open-note/${ relpath }`)
}


import { useIntervalFn } from '@vueuse/core'

useIntervalFn(refresh, 5000)
</script>


<template>
<div>
  <div class="title">最近打开</div>
  <el-scrollbar max-height="32vh">
    <div class="notes-container">
      <div class="note" v-for="note in recentOpenList" @click="open(note.relpath)">{{ note.name }}</div>
    </div>
  </el-scrollbar>
</div>
</template>


<style scoped>
.title {
  color: white;
  font-size: 28px;
  background-color: #FFFFFF01;
}

.notes-container {
  padding-left: 10px;
  background-color: #FFFFFF01;
}
.note {
  color: white;
}
.note:hover {
  background-color: #F5F5F540;
}
</style>
