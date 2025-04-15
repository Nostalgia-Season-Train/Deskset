<script setup>
/* === 个性资料 === */
import { ref } from 'vue'

const profileAvatar = ref('')
const profileDate = ref({ name: '', bio: '' })


/* === 热力图 === */
  // 解决 undefined is not imported 报错
  // 1、加入 import * as echarts from 'echarts'
  // 2、去掉 lang="ts"
import VChart from 'vue-echarts'
import * as echarts from 'echarts'

import dayjs from 'dayjs'

const weeknum = 28  // 起始日期 ~ 结束日期：前 weeknum 周周一 ~ 今天
const heatMaxNum = 10  // h.number 不超过 heatmapChart.visualMap.max

// { date: 'YYYYMMDD', number: int } 转换成 ECharts 热力图格式 ['YYYY-MM-DD', int]
const convert = async (heats) => {
  return heats.map(h => { return [dayjs(h.date, 'YYYYMMDD').format('YYYY-MM-DD'), h.number < heatMaxNum ? h.number : heatMaxNum] })
}

const heatmapChart = ref({
  tooltip: {},  // 鼠标移入，显示当天数据
  visualMap: {
    min: 0, max: heatMaxNum,
    show: false,  // 关闭标题
    inRange: { color: ['#FFF', '#388E3C'] }  // heat(cell) 热点颜色
  },
  calendar: {
    left: 5, right: null, top: 5, bottom: null,  // 类似 padding，right、bottom 设为 null 避免拉伸
    cellSize: 12,
    range: [dayjs().subtract(weeknum, 'week').startOf('isoWeek').format('YYYY-MM-DD'), dayjs().format('YYYY-MM-DD')]
  },
  series: {
    type: 'heatmap',
    coordinateSystem: 'calendar',
    data: []
  }
})


/* === 刷新 === */
import { inject } from 'vue'

const axios = inject('$axios')
const refresh = async () => {
  profileAvatar.value = URL.createObjectURL((await axios.get('/v0/note/obsidian/profile/avatar', { responseType: 'blob' })).data)
  profileDate.value = (await axios.get('/v0/note/obsidian/profile/data')).data.result

  const heats = await convert((await axios.get(`/v0/note/obsidian/stats/heatmap/${weeknum}`)).data.result)
  heatmapChart.value.calendar.range = [heats[0][0], heats[heats.length - 1][0]]
  heatmapChart.value.series.data = heats
}
refresh()
</script>


<template>
<body>
  <aside class="profile">
    <img :src="profileAvatar" style="width: 100px; height: 100px;">
    <div class="name">{{ profileDate.name }}</div>
    <div class="bio">{{ profileDate.bio }}</div>
  </aside>
  <main>
    <v-chart
      class="heatmap"
      :option="heatmapChart"
      style="width: 650px; height: 500px;"
    />
  </main>
</body>
</template>
