<script lang="ts" setup>
import { ref, inject } from 'vue'
import { Axios } from 'axios'
import { ElScrollbar } from 'element-plus'
import { History } from 'lucide-vue-next'

const axios = inject('$axios') as Axios

const recents = ref()

const open = async (path: string) => {
  axios.get(`/v0/note/obsidian/common/open?path=${ path }`)
}


/* === 刷新 === */
const refresh = async () => {
  const data = (await axios.get('/v0/note/obsidian/common/recent-notes')).data
  recents.value = data.result
}
refresh()
</script>


<template>
<div class="container">
  <div class="title">
    <History /><span>最近打开</span>
  </div>
  <el-scrollbar class="recents" max-height="240px">
    <div class="note" v-for="note in recents" @click="open(note?.path)">{{ note?.name }}</div>
  </el-scrollbar>
</div>
</template>


<style lang="less" scoped>
.container {
  width: 220px;
  background-color: #FFF3;
  border-radius: 5px;
}

.title {
  display: flex;
  align-items: center;
  gap: 5px;
  color: white;

  svg {
    width: 24px;
    height: 24px;
  }
  span {
    font-size: 18px;
  }
}

.recents {
  padding: 3px;
  color: white;

  .note:hover {
    background-color: #F5F5F540;
  }
}
</style>
