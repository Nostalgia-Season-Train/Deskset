<script lang="ts" setup>
import { ref } from 'vue'
import { Cpu, MemoryStick, HardDrive } from 'lucide-vue-next'

const cpu_percent = ref(50)
const ram_percent = ref(50)
const disk_percent = ref(50)


/* === 轮询 === */
import axios from 'axios'
import { useIntervalFn } from '@vueuse/core'

const refresh = async () => {
  const data = (await axios.get('/v0/device/realtime')).data
  cpu_percent.value = data.result.cpu.percent
  ram_percent.value = data.result.ram.percent
  disk_percent.value = data.result.disk.percent
}

refresh()
useIntervalFn(refresh, 1200)
</script>


<template>
<div class="container">

  <div class="progress">
    <div>
      <Cpu/>
      <div>{{ cpu_percent.toFixed(1) }}</div>
      <div>CPU</div>
    </div>
    <div class="ring cpu-ring"></div>
  </div>

  <div class="progress">
    <div>
      <MemoryStick/>
      <div>{{ ram_percent.toFixed(1) }}</div>
      <div>RAM</div>
    </div>
    <div class="ring ram-ring"></div>
  </div>

  <div class="progress">
    <div>
      <HardDrive/>
      <div>{{ disk_percent.toFixed(1) }}</div>
      <div>DISK</div>
    </div>
    <div class="ring disk-ring"></div>
  </div>

</div>
</template>


<style scoped>
.container {
  padding: 3px;

  display: flex;
  gap: 15px;
}

.progress {
  position: relative;
  width: 70px;
  height: 70px;

  display: flex;
  justify-content: center;
  align-items: center;

  color: white;
  text-align: center;
}
.progress>div>div:nth-child(3) {
  position: absolute;
  top: 75px;
  left: 50%;
  transform: translateX(-50%);
}

.ring {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 5px solid #FFF;
  border-radius: 50%;
}
.ring.cpu-ring {
  mask-image: conic-gradient(#FFF v-bind((cpu_percent / 100) * 360 + 'deg'), #FFF5 0deg);
}
.ring.ram-ring {
  mask-image: conic-gradient(#FFF v-bind((ram_percent / 100) * 360 + 'deg'), #FFF5 0deg);
}
.ring.disk-ring {
  mask-image: conic-gradient(#FFF v-bind((disk_percent / 100) * 360 + 'deg'), #FFF5 0deg);
}
</style>
