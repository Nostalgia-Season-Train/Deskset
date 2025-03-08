<script setup>
/* 表格样式 */
import VChart from "vue-echarts"
import * as echarts from "echarts"  // 不加报错 undefined is not imported

const option = {
  animation: false,
  color: "#FFF",
  // left right -3 盖住图表跟轮廓间空隙
  grid: { top: 0, bottom: 0, left: -3, right: -3 },
  xAxis: {
    show: false,
    type: "category"
  },
  yAxis: {
    max: 100, min: 0,
    show: false
  },
  series: {
    data: Array(30).fill(0),
    type: "line",
    showSymbol: false,
    lineStyle: { width: 1 },
    areaStyle: {
      opacity: 0.35,
      color: self.color
    }
  }
}


/* 查询函数 */
import { ref } from 'vue'
import { desksetReq } from '../request'

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
  const resCPU = await desksetReq.get("/v0/device/cpu")
  numCPU.value = resCPU.data.data.percent
  optionCPU.value.series.data.shift()
  optionCPU.value.series.data.push(resCPU.data.data.percent)

  const resMemory = await desksetReq.get("/v0/device/memory")
  numMemory.value = resMemory.data.data.percent
  optionMemory.value.series.data.shift()
  optionMemory.value.series.data.push(resMemory.data.data.percent)

  const resDisk = await desksetReq.get("/v0/device/disk-useage")
  numDisk.value = resDisk.data.data
  optionDisk.value.series.data.shift()
  optionDisk.value.series.data.push(resDisk.data.data)

  const resNetwork = await desksetReq.get("/v0/device/network")
  numNetwork.value = resNetwork.data.data
  optionNetwork.value.series.data.shift()
  optionNetwork.value.series.data.push(resNetwork.data.data.recv)
}
device()


/* 轮询 */
import { useIntervalFn } from '@vueuse/core'

useIntervalFn(device, 1000)
</script>


<template>
<div class="color-watch"><!-- 不加警告 v-model -->
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #42A5F5;">
      <v-chart :option="optionCPU" />
    </div>
    <div>
      <div class="text">CPU</div>
      <div class="num">{{ numCPU }}%</div>
    </div>
  </div>
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #AB47BC;">
      <v-chart :option="optionMemory" />
    </div>
    <div>
      <div class="text">Memory</div>
      <div class="num">{{ numMemory }}%</div>
    </div>
  </div>
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #66BB6A;">
      <v-chart :option="optionDisk" />
    </div>
    <div>
      <div class="text">Disk</div>
      <div class="num">{{ numDisk }}%</div>
    </div>
  </div>
  <div class="watch">
    <div style="width: 100px; height: 70px; pointer-events: none; outline: 1px solid #FFCA28;">
      <v-chart :option="optionNetwork" />
    </div>
    <div>
      <div class="text">Network</div>
      <div class="num">S: {{ numNetwork.sent }}.0 Kbps</div>
      <div class="num">R: {{ numNetwork.recv }}.0 Kbps</div>
    </div>
  </div>
</div>
</template>


<style scoped>
.color-watch {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);

  padding: 5px;

  background-color: #0005;
  border: 1px solid #777;
}

.watch {
  width: 200px;

  display: flex;
  justify-content: left;
  gap: 5px;

  margin: 5px;
}

.text {
  font-size: 16px;
  color: #FFF;
}
.num {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;  /* 避免换行撑开高度 */
}
</style>
