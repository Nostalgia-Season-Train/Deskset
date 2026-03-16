<script setup>
/* ==== 注意事项 ==== */
// Components 插件不会计入自身
  // 也就是 .components 文件的创建编辑情况
  // 所以热力图可能不一样


/* ==== Echart 声明 ==== */
import { ref } from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts'
import { SVGRenderer } from 'echarts/renderers'
import dayjs from 'dayjs'

echarts.use([SVGRenderer])

const weeknum = 28  // 统计周数

const heatChart = ref({
  tooltip: {
    // 悬停时显示热点值
  },
  visualMap: {
    // 热点范围 0 ~ 10
    min: 0, max: 10,
    // 热点颜色 #FFF ~ #388E3C，热点不透明度 0 ~ 1
    inRange: { color: ['#FFF', '#388E3C'], opacity: [0, 1] },
    // 隐藏左侧图例
    show: false
  },
  calendar: {
    // 设置纵向热力图
    orient: 'vertical',
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
    ],
    // 去掉容器边框
    splitLine: { show: false },
    // 底部背景色，底部边框色，底部边框宽度
    itemStyle: { color: '#0000', borderColor: '#0000', borderWidth: 0 }
  },
  series: {
    // 选择热力图
    type: 'heatmap',
    // 绑定热力图到日历
    coordinateSystem: 'calendar',
    // 热力图热点数据，会被 refresh 刷新
    data: [],
    // 去掉元素边框 2（热点边框）
    itemStyle: { borderWidth: 0 }
  }
})


/* ==== 刷新 ==== */
import axios from 'axios'

const refresh = async () => {
  const rawHeats = (await axios.post(`/v0/note/obsidian/stats/heatmap`, {
    start_day: dayjs().startOf('month').format('YYYYMMDD'),
    end_day: dayjs().endOf('month').format('YYYYMMDD')
  })).data.result
  const heats = rawHeats.map(heat => [dayjs(heat.day, 'YYYYMMDD').format('YYYY-MM-DD'), heat.num])
  heatChart.value.calendar.range = [heats[0][0], heats[heats.length - 1][0]]
  heatChart.value.series.data = heats
}
refresh()
</script>


<template>
<div class="heatmap">
  <!-- svg 渲染不随缩放模糊 -->
  <VChart
    class="heatmap"
    :option="heatChart"
    :initOptions='{ renderer: "svg" }'
    style="width: 100%; height: 100%;"
  />
</div>
</template>


<style lang="less" scoped>
.heatmap {
  width: 450px;
  height: 120px;
}
</style>
