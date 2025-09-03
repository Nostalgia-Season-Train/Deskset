<script lang="ts" setup>
import { ref } from 'vue'
import { marked } from 'marked'
import axios from 'axios'

const render = new marked.Renderer()
// 禁用外部链接
render.link = (href) => {
  return `<a href="#">${href.href}</a>`
}

const name = ref('')
const path = ref('')
const content = ref()

const refresh = async () => {
  const response = await axios.get('/v0/note/obsidian/diary/today')
  const diary = response.data.result
  if (diary == null)
    return
  name.value = diary.name
  path.value = diary.path
  content.value.innerHTML = marked(diary.content, {
    renderer: render,
    breaks: true  // 允许单换行符换行
  })
}
refresh()

const openInObsidian = async () => {
  if (path.value != '')
    await axios.get(`/v0/note/obsidian/common/open-in-obsidian?path=${path.value}`)
}


/* ==== 轮询 ==== */
import { useInterval } from 'vue-hooks-plus'

useInterval(refresh, 3 * 60 * 1000)


/* ==== 子组件 ==== */
import { ElScrollbar } from 'element-plus'
</script>


<template>
<div class="diary">
  <div class="name">
    <span v-if="name != ''">{{ name }}</span>
    <span v-else>暂无今日日记</span>
  </div>
  <div class="content" @dblclick="openInObsidian">
    <ElScrollbar>
      <div ref="content"></div>
    </ElScrollbar>
  </div>
</div>
</template>


<style lang="less" scoped>
* {
  box-sizing: border-box;
}

.diary {
  width: 270px;
  height: 250px;

  color: #000;
  background: #FFFD;
  box-shadow: 0 2px 4px #000A;

  // ElScrollbar 高度自适应，建议结合怪异盒子模型使用
  display: flex;
  flex-direction: column;
  .content {
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  .name {
    width: 100%;
    height: 30px;
    background: orange;
    padding-left: 5px;
    display: flex;
    align-items: center;
    span {
      position: relative;
      top: -1px;
    }
  }

  :deep(*) {
    margin: 0;
  }
  :deep(a) {
    color: rgb(224, 224, 224);
  }
  :deep(ul) {
    padding-left: 30px;
  }
}
</style>
