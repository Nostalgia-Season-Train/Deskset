<script setup>
import { ref } from "vue"
import { desksetReq } from '../request'

const disks = ref()

const disk = async () => {
  const response_disk = await desksetReq.get("/v0/device/disk")
  disks.value = response_disk.data.data
}
disk()


import { useIntervalFn } from "@vueuse/core"

useIntervalFn(disk, 60000)
</script>


<template>
<div>
  <div class="disks" v-for="disk in disks">
    <div class="progress" :style="`background-size: ${disk.percent}%;`"></div>
    <div style="display: flex;">
      <span class="root" style="font-size: 14px;">{{ disk.root }}</span>
      <span class="split">&nbsp;&nbsp;</span>
      <span class="num"  style="font-size: 12px;">{{ disk.free }}&nbsp;GB&nbsp;可用，共&nbsp;{{ disk.total }}&nbsp;GB</span>
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
  height: 5.6px;
  background-image: linear-gradient(#FFF 0 0);
  background-color: rgba(128, 128, 128, 0.35);
  background-position-x: 0px;
  background-repeat: no-repeat;
}
</style>
