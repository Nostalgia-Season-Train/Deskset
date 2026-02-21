<script setup>
import { ref } from 'vue'
import axios from 'axios'

const disks = ref()

const disk = async () => {
  const result = (await axios.get('/v0/device/disk')).data.result
  disks.value = result
}
disk()


import { useIntervalFn } from '@vueuse/core'

useIntervalFn(disk, 60000)
</script>


<template>
<div>
  <div class="disks" v-for="disk in disks">
    <div class="progress" :style="`background-size: ${disk.percent}%;`"></div>
    <div style="display: flex;">
      <span class="root" style="font-size: 16px;">{{ disk.root }}</span>
      <span class="split">&nbsp;&nbsp;</span>
      <span class="num" style="font-size: 14px;">{{ disk.free.toFixed(1) }}&nbsp;GB&nbsp;可用，共&nbsp;{{ disk.total.toFixed(1) }}&nbsp;GB</span>
    </div>
  </div>
</div>
</template>


<style scoped>
.disks {
  color: white;
  margin-bottom: 10px;
}

.disks>.progress {
  width: 280px;
  height: 5px;
  background-image: linear-gradient(#FFF 0 0);
  background-color: rgba(128, 128, 128, 0.35);
  background-position-x: 0px;
  background-repeat: no-repeat;
}
</style>
