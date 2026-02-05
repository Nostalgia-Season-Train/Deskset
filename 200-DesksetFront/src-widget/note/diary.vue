<script lang="ts" setup>
import { ref, computed } from 'vue'
import { marked } from 'marked'
import axios from 'axios'
import dayjs from 'dayjs'

const render = new marked.Renderer()
// 禁用外部链接
render.link = (href) => {
  return `<a href="#">${href.href}</a>`
}

const name = ref('')
const path = ref('')
const content = ref()

const dateRaw = ref(new Date())
const date = computed({
  get() {
    return dateRaw.value
  },
  async set(newValue) {
    dateRaw.value = newValue
    await refresh()
  }
})

const refresh = async () => {
  const response = await axios.get(`/v0/note/obsidian/diary/read-day/${dayjs(dateRaw.value).format('YYYYMMDD')}`)
  const diary = response.data.result
  if (diary == null) {
    content.value.innerHTML = marked('')
    return
  }
  name.value = diary.name
  path.value = diary.path
  content.value.innerHTML = marked(diary.content, {
    renderer: render,
    breaks: true  // 允许单换行符换行
  })
}
refresh()

const diaryIDList = ref<any>([])
const refreshPanel = async (date: Date) => {
  const response = await axios.get(`/v0/note/obsidian/diary/read-month/${dayjs(date).format('YYYYMM')}`)
  diaryIDList.value = response.data.result.map((item: any) => item.id)
}
refreshPanel(new Date())

const openInObsidian = async () => {
  if (path.value != '')
    await axios.get(`/v0/note/obsidian/common/open-in-obsidian?path=${path.value}`)
}


/* ==== 轮询 ==== */
import { useInterval } from 'vue-hooks-plus'

useInterval(refresh, 3 * 60 * 1000)


/* ==== 子组件 ==== */
import { ElScrollbar, ElDatePicker } from 'element-plus'
</script>


<template>
<div class="diary">
  <ElDatePicker
    v-model="date"
    type="date"
    @panel-change="refreshPanel"
  >
    <template #default="cell">
      <div class="cell">
        <!-- cell.renderText != null 时显示的是月份 -->
        <span class="text">{{ cell.renderText != null ? cell.renderText : cell.text }}</span>
        <span class="mark" v-if="cell.dayjs != null ? diaryIDList.includes(cell.dayjs.format('YYYYMMDD')) : false"></span>
      </div>
    </template>
  </ElDatePicker>
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

  :deep(.el-input) {
    width: 100%;
    height: 30px;
    .el-input__wrapper {
      padding-left: 5px;
      display: flex;
      align-items: center;
      background: orange;
      border: none;
      border-radius: 0;
      box-shadow: none;
      .el-icon {
        color: #000;
        font-size: 16px;
      }
      input {
        margin: 5px;
        color: #000;
        font-size: 16px;
      }
    }
  }
}

// ElDatePicker 弹出的日期面板是 body 不是 .diary 子元素
.cell>.mark {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  background: var(--el-color-primary);
  border-radius: 50%;
}
</style>
