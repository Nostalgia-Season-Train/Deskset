<script setup>
import VChart from "vue-echarts"
import * as echarts from "echarts"

const option = {
  animation: false,
  color: ["#FFFFFF"],
  // bottom 5 把线抬起来
  grid: { top: 0, bottom: 5, left: 0, right: 0 },
  xAxis: {
    show: false,
    type: "category"
  },
  yAxis: {
    max: 100, min: 0,
    show: false
  },
  series: {
    data: Array(40).fill(0),
    type: "line",
    showSymbol: false,
    lineStyle: { width: 1 },
    areaStyle: {
      opacity: 0.8,
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: "rgba(255, 255, 255, 1)" },
        { offset: 1, color: "rgba(255, 255, 255, 0)" }
      ])
    }
  }
}


import { ref } from "vue"
import { desksetReq } from '../request'

const cpu_percent = ref(0)
const optionCPU = ref(structuredClone(option))

const memory_percent = ref(0)
const optionRAM = ref(structuredClone(option))

const device = async () => {
  const response_cpu = await desksetReq.get("/v0/device/cpu")
  cpu_percent.value = response_cpu.data.data.percent
  optionCPU.value.series.data.shift()
  optionCPU.value.series.data.push(response_cpu.data.data.percent)

  const response_memory = await desksetReq.get("/v0/device/memory")
  memory_percent.value = response_memory.data.data.percent
  optionRAM.value.series.data.shift()
  optionRAM.value.series.data.push(response_memory.data.data.percent)
}
device()


import { useIntervalFn } from "@vueuse/core"

useIntervalFn(device, 1000)
</script>


<template>
  <div class="device">
    <div class="cpu">
      <!-- pointer-events: none 不需要与图表交互 -->
      <div style="width: 250px; height: 70px; pointer-events: none;">
        <v-chart :option="optionCPU" />
      </div>
      <span class="text">CPU</span>
      <span class="split">&nbsp;</span>
      <span class="cpu-num">{{ cpu_percent }}%</span>
    </div>
    <div class="memory">
      <div style="width: 250px; height: 70px; pointer-events: none;">
        <v-chart :option="optionRAM" />
      </div>
      <span class="text">RAM</span>
      <span class="split">&nbsp;</span>
      <span class="num">{{ memory_percent }}%</span>
    </div>
  </div>
</template>


<style scoped>
.device {
  color: white;
}
</style>
