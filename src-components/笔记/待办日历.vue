<script lang="ts" setup>
/* === FullCalendar 选项 === */
import { reactive } from 'vue'

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import zhchLocale from '@fullcalendar/core/locales/zh-cn'

const calendarOptions = reactive({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  locale: zhchLocale,
  events: [],
  datesSet: async () => refresh()  // 用户切换月份，触发回调更新
})


/* === 定时刷新 === */
import { ref } from 'vue'
const refFC = ref()

import { getDesksetReq } from '../request'
const desksetReq = await getDesksetReq()

import dayjs from 'dayjs'

const refresh = async () => {
  const api = refFC.value?.getApi()
  if (api == undefined) {
    return
  }

  calendarOptions.events = []  // 清空上次任务

  const date = api.getDate()
  const month = dayjs(date).format('YYYYMM')

  const diarys = (await desksetReq.get(`/v0/note/obsidian/diary/read-month/${month}`)).data.result
  for (const diary of diarys) {        // 读取日记列表
    for (const task of diary.tasks) {  // 读取日记中的任务列表
      calendarOptions.events.push({ title: task.text, start: diary.id })
    }
  }
}

import { onMounted } from 'vue'
onMounted(async () => refresh())  // 组件挂载后刷新，否则 refFC.getApi() 为空
</script>


<template>
<div>
  <FullCalendar ref="refFC" :options='calendarOptions'/>
</div>
</template>


<style lang="less" scoped>
.fc {
  width: 700px;
  height: 500px;

  color: white;
}
</style>
