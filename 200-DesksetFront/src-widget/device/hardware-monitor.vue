<script setup>
/* 表格样式 */
import VChart from 'vue-echarts'
import * as echarts from 'echarts'  // 不加报错 undefined is not imported
import { SVGRenderer } from 'echarts/renderers'

echarts.use([SVGRenderer])

const option = {
  animation: false,
  color: '#FFF',
  // left right -3 盖住图表跟轮廓间空隙
  grid: { top: 0, bottom: 0, left: -3, right: -3 },
  xAxis: {
    show: false,
    type: 'category'
  },
  yAxis: {
    max: 100, min: 0,
    show: false
  },
  series: {
    data: Array(30).fill(0),
    type: 'line',
    showSymbol: false,
    lineStyle: { width: 1 },
    areaStyle: {
      opacity: 0.35,
      color: self.color
    }
  },
  backgroundColor: '#FFF0'
}


/* 查询函数 */
import { ref } from 'vue'
import axios from 'axios'

const numCPU = ref(0)
const optionCPU = ref(structuredClone(option))
optionCPU.value.color = '#42A5F5'

const numMemory = ref(0)
const optionMemory = ref(structuredClone(option))
optionMemory.value.color = '#AB47BC'

const numDisk = ref(0)
const optionDisk = ref(structuredClone(option))
optionDisk.value.color = '#66BB6A'

const numNetwork = ref({ sent: 0, recv: 0 })
const optionNetwork = ref(structuredClone(option))
optionNetwork.value.color = '#FFCA28'
optionNetwork.value.yAxis.max = 1000

const device = async () => {
  const result = (await axios.get('/v0/device/monitor')).data.result

  numCPU.value = result.cpu.percent
  optionCPU.value.series.data.shift()
  optionCPU.value.series.data.push(numCPU.value)

  numMemory.value = result.ram.percent
  optionMemory.value.series.data.shift()
  optionMemory.value.series.data.push(numMemory.value)

  numDisk.value = result.disk.percent
  optionDisk.value.series.data.shift()
  optionDisk.value.series.data.push(numDisk.value)

  numNetwork.value = {
    sent: (result.network.sent / 1000).toFixed(1),
    recv: (result.network.recv / 1000).toFixed(1)
  }
  optionNetwork.value.series.data.shift()
  optionNetwork.value.series.data.push(numNetwork.value.recv)
}
device()


/* 轮询 */
import { useIntervalFn } from '@vueuse/core'

useIntervalFn(device, 1200)
</script>


<template>
<div class="color-watch"><!-- 不加警告 v-model -->
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #42A5F5;">
      <v-chart :option="optionCPU" :initOptions='{ renderer: "svg" }'/>
    </div>
    <div>
      <div class="text">CPU</div>
      <div class="num">{{ numCPU }}%</div>
    </div>
  </div>
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #AB47BC;">
      <v-chart :option="optionMemory" :initOptions='{ renderer: "svg" }'/>
    </div>
    <div>
      <div class="text">RAM</div>
      <div class="num">{{ numMemory }}%</div>
    </div>
  </div>
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #66BB6A;">
      <v-chart :option="optionDisk" :initOptions='{ renderer: "svg" }'/>
    </div>
    <div>
      <div class="text">Disk</div>
      <div class="num">{{ numDisk }}%</div>
    </div>
  </div>
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #FFCA28;">
      <v-chart :option="optionNetwork" :initOptions='{ renderer: "svg" }'/>
    </div>
    <div>
      <div class="text">Network</div>
      <div class="num">S: {{ numNetwork.sent }}Mbps</div>
      <div class="num">R: {{ numNetwork.recv }}Mbps</div>
    </div>
  </div>
</div>
</template>


<style lang="less" scoped>
@import '../style.less';

.color-watch {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);

  padding: 5px;

  .dsw-box();
  background: #3336;
  border: solid #CCCA 1px;
}

.watch {
  width: 200px;

  display: flex;
  justify-content: left;
  gap: 5px;

  margin: 5px;
}

.text {
  .dsw-text();
  color: #FFF;
  font-weight: 300;
}
.num {
  width: 90px;
  .dsw-text-title();
  color: #FFF9;
  font-size: 14px;
  font-weight: 300;
  font-feature-settings: 'ss01', 'tnum';
  white-space: nowrap;  /* 避免换行撑开高度 */
  overflow: hidden;
}
</style>
