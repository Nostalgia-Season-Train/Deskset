<script lang="ts" setup>
import { ref } from 'vue'
import { getDesksetReq } from '../request'

const per = ref('50')

const device = async () => {
  const desksetReq = await getDesksetReq()
  const rep = await desksetReq.get("/v0/device/memory")
  per.value = rep.data.data.percent
}
device()


import { useIntervalFn } from '@vueuse/core'

useIntervalFn(device, 1000)
</script>


<template>
<div>
  <div class="container">
    <div>
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-memory-stick"><path d="M6 19v-3"/><path d="M10 19v-3"/><path d="M14 19v-3"/><path d="M18 19v-3"/><path d="M8 11V9"/><path d="M16 11V9"/><path d="M12 11V9"/><path d="M2 15h20"/><path d="M2 7a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v1.1a2 2 0 0 0 0 3.837V17a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-5.1a2 2 0 0 0 0-3.837Z"/></svg>
      <div>{{ per }}</div>
    </div>
    <div class="ring"></div>
  </div>
</div>
</template>


<!-- less 影响 v-bind -->
<style scoped>
.container {
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
  left: -5px;
  top: -5px;

  width: 100%;
  height: 100%;
  border: 5px solid #FFF;
  border-radius: 50%;

  /* 圆环进度条实现：蒙版 alpha 乘以 元素 alpha */
  mask-image: conic-gradient(#FFF v-bind((per / 100) * 360 + 'deg'), transparent 0deg);
}
</style>
