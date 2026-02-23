<script setup>
import { ref } from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts'
import dayjs from 'dayjs'

const weeknum = 28  // 统计周数

const heatChart = ref({
  tooltip: {
    // 悬停时显示热点值
  },
  visualMap: {
    // 热点范围 0 ~ 10
    min: 0, max: 10,
    // 热点颜色 #FFF ~ #388E3C
    inRange: { color: ['#FFF', '#388E3C'] },
    // 隐藏左侧图例
    show: false
  },
  calendar: {
    // 热点大小 15
    cellSize: 15,
    // 居中图表
    left: 'center', top: 'center',
    // 隐藏左侧星期
    dayLabel: { show: false },
    // 隐藏上方月份
    monthLabel: { show: false },
    // 隐藏左侧年份
    yearLabel: { show: false },
    // 日期范围，会被 refresh 刷新
    range: [
      dayjs().subtract(weeknum, 'week').startOf('isoWeek').format('YYYY-MM-DD'),
      dayjs().format('YYYY-MM-DD')
    ]
  },
  series: {
    // 选择热力图
    type: 'heatmap',
    // 绑定热力图到日历
    coordinateSystem: 'calendar',
    // 热力图热点数据，会被 refresh 刷新
    data: []
  }
})


/* ==== 刷新 ==== */
import axios from 'axios'

const refresh = async () => {
  const rawHeats = (await axios.post(`/v0/note/obsidian/stats/heatmap`, {
    start_day: dayjs().subtract(weeknum, 'week').startOf('week').format('YYYYMMDD'),
    end_day: dayjs().format('YYYYMMDD')
  })).data.result
  const heats = rawHeats.map(heat => [dayjs(heat.date, 'YYYYMMDD').format('YYYY-MM-DD'), heat.number])
  heatChart.value.calendar.range = [heats[0][0], heats[heats.length - 1][0]]
  heatChart.value.series.data = heats
}
refresh()
</script>


<template>
<div class="heatmap">
  <VChart
    class="heatmap"
    :option="heatChart"
    style="width: 100%; height: 100%;"
  />
</div>
</template>


<style lang="less" scoped>
.heatmap {
  width: 450px;
  height: 120px;
  background: #FFF;
}
</style>
