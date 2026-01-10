<script lang="ts" setup>
import { ref } from 'vue'

const whichPart = ref('activity')

const thinos = ref()   // 动态（Thino）
const tasks = ref()    // 打卡（任务）
const content = ref()  // 内容（日记文件，除了属性之外的文本）


import { getDesksetReq } from './request'

const desksetReq = await getDesksetReq()
const refresh = async () => {
  const rep = await desksetReq.get('/v0/note/obsidian/diary/today')
  thinos.value = rep.data.result.thinos
  tasks.value = rep.data.result.tasks
  content.value = rep.data.result.content
}
refresh()
</script>


<template>
<div class="container">
  <nav>
    <div @click="whichPart='activity'">动态</div>
    <div @click="whichPart='todo'">打卡</div>
    <div @click="whichPart='content'">内容</div>
  </nav>
  <main>
    <div v-if="whichPart == 'activity'">
      <div v-for="thino in thinos">
        <div>{{ thino.create }}</div>
        <div>{{ thino.content }}</div>
      </div>
    </div>
    <div v-if="whichPart == 'todo'">
      <div v-for="task in tasks">
        <input type="radio"/><span>{{ task.text }}</span>
      </div>
    </div>
    <div v-if="whichPart == 'content'">
      <div>{{ content }}</div>
    </div>
  </main>
</div>
</template>


<style lang="less" scoped>
.container {
  -webkit-app-region: drag;
}

.container {
  width: 100%;
  height: 100%;
  background-color: #FFFFFFA0;

  display: flex;
  justify-content: space-between;

  nav {
    color: black;
    background-color: white;
    div:hover {
      color: gray;
    }
  }

  main {
    flex: 1;
  }
}
</style>
