<script lang="ts" setup>
import { ref } from 'vue'
import { Cpu, MemoryStick } from 'lucide-vue-next'

const cpu_percent = ref('50')
const ram_percent = ref('50')


/* === 轮询 === */
import { inject } from 'vue'
import { Axios } from 'axios'
import { useIntervalFn } from '@vueuse/core'

const axios = inject('$axios') as Axios
const refresh = async () => {
  const data = (await axios.get('/v0/device/realtime')).data
  cpu_percent.value = data.result.cpu.percent
  ram_percent.value = data.result.ram.percent
}

refresh()
useIntervalFn(refresh, 1200)
</script>


<template>
<div class="container">
  <div class="progress">
    <div>
      <Cpu />
      <div>{{ cpu_percent }}</div>
    </div>
    <div class="ring cpu-ring"></div>
  </div>
  <div class="progress">
    <div>
      <MemoryStick />
      <div>{{ ram_percent }}</div>
    </div>
    <div class="ring ram-ring"></div>
  </div>
</div>
</template>


<style scoped>
.container {
  padding: 3px;

  display: flex;
  gap: 5px;

  background-color: #FFF3;
  border-radius: 5px;
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

.ring {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 5px solid #FFF;
  border-radius: 50%;
}
.ring.cpu-ring {
  mask-image: conic-gradient(#FFF v-bind((cpu_percent / 100) * 360 + 'deg'), transparent 0deg);
}
.ring.ram-ring {
  mask-image: conic-gradient(#FFF v-bind((ram_percent / 100) * 360 + 'deg'), transparent 0deg);
}
</style>
