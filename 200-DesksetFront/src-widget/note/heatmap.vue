<script setup>
/* ==== 注意事项 ==== */
// Components 插件不会计入自身
  // 也就是 .components 文件的创建编辑情况
  // 所以热力图可能不一样


/* ==== 图标总数范围 ==== */
import { ref } from 'vue'
import { FileEdit } from 'lucide-vue-next'

const total = ref(0)    // 热点累加总数
const weeknum = ref(4)  // 统计周数


/* ==== Echart 声明 ==== */
import VChart from 'vue-echarts'
import * as echarts from 'echarts'
import { SVGRenderer } from 'echarts/renderers'
import dayjs from 'dayjs'
import isoWeek from 'dayjs/plugin/isoWeek'
dayjs.extend(isoWeek)  // dayjs().startOf('isoWeek') 需要此插件

echarts.use([SVGRenderer])

const heatChart = ref({
  tooltip: {
    // 悬停时显示热点值
    formatter: (p) => {
      const fmtDay = dayjs(p.data[0], 'YYYY-MM-DD').format('YYYY/MM/DD-dddd')
      const num = p.data[1]
      return `${fmtDay}: ${num}`
    }
  },
  visualMap: {
    // 热点范围 0 ~ 10
    min: 0, max: 10,
    // 热点颜色 #FFF ~ #388E3C，热点不透明度 1 ~ 1
    inRange: { color: ['#FFF', '#388E3C'], opacity: [1, 1] },
    // 隐藏图例
    // show: false,
    // 图例位置
    top: 'middle',  // 上下居中
    right: 4,
    // 图例容器：内边距，宽度，高度
    padding: 0,
    itemWidth: 8,
    itemHeight: 16 * 7,
    // 关闭悬停文本和悬停游标
    hoverLink: false,
  },
  calendar: {
    // 设置纵向热力图
    // orient: 'vertical',
    // 热点大小 16
    cellSize: 16,
    // 居中图表
    // (父容器宽度 - 图例宽度) - (热点大小 * 5) = 可用空隙
    // left: ((160 - 8) - (16 * 5)) / 2, top: 'middle',
    // 图例宽度 + 星期文本与热力图距离 + 图例与图表容器右边距离，上下居中
    right: 8 + 4 + 4, top: 'middle',
    // 星期配置
    dayLabel: {
      show: true,   // 显示左侧星期
      firstDay: 1,  // 从星期一开始
      margin: 4,    // 文本与热力图距离
    },
    // 隐藏上方月份
    monthLabel: { show: false },
    // 隐藏左侧年份
    yearLabel: { show: false },
    // 日期范围，会被 refresh 刷新
    range: [
      dayjs().subtract(weeknum.value, 'week').startOf('isoWeek').format('YYYY-MM-DD'),
      dayjs().format('YYYY-MM-DD')
    ],
    // 去掉容器边框
    splitLine: { show: false },
    // 底部背景色，底部边框色，底部边框宽度
    itemStyle: { color: '#0000', borderColor: '#0000', borderWidth: 2 }
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
    // 范围：本月
    // start_day: dayjs().startOf('month').format('YYYYMMDD'),
    // end_day: dayjs().endOf('month').format('YYYYMMDD')
    // 范围：本周 + 前 weeknum 周
    start_day: dayjs().subtract(weeknum.value, 'week').startOf('isoWeek').format('YYYYMMDD'),
    end_day: dayjs().format('YYYYMMDD')
  })).data.result
  const heats = rawHeats.map(heat => [dayjs(heat.day, 'YYYYMMDD').format('YYYY-MM-DD'), heat.num])
  total.value = rawHeats.reduce((acc, heat) => acc + heat.num, 0)
  heatChart.value.calendar.range = [heats[0][0], heats[heats.length - 1][0]]
  heatChart.value.series.data = heats
}
refresh()
</script>


<template>
<div class="heatmap">

  <div class="left">
    <div class="title">
      <FileEdit/>
      <span>编辑数量</span>
    </div>
    <div>总数：{{ total }}</div>
    <div>范围：前 {{ weeknum }} 周</div><!-- 包括本周，文本太长放不下 -->
  </div>

  <div class="echart__wrapper">
    <!-- svg 渲染不随缩放模糊 -->
    <VChart
      :option="heatChart"
      :initOptions='{ renderer: "svg" }'
    />
  </div>

</div>
</template>


<style lang="less" scoped>
@import '../style.less';

.heatmap {
  width: 240px;
  height: 120px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  .dsw-box();

  .left {
    padding: 4px 0 0 4px;
    height: 100%;
    .title {
      display: flex;
      align-items: center;
    }
  }
  .echart__wrapper {
    width: 120px;
    height: 120px;
  }
}
</style>
