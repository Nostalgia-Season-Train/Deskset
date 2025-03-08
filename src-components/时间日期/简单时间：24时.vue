<script setup>
import { ref } from "vue"
import { desksetReq } from '../request'

const hour   = ref("00")
const minute = ref("00")

const time = async () => {
  const response = await desksetReq.get('/v0/datetime/time')
  hour.value = response.data.data.hour
  minute.value = response.data.data.minute
}
time()


import { useIntervalFn } from "@vueuse/core"

useIntervalFn(time, 250)
</script>


<template>
  <div class="time">
    <span class="hour-minute">{{ hour }}:{{ minute }}</span>
  </div>
</template>


<style scoped>
.time {
  color: white;
}

.time>.hour-minute {
  font-size: 80px;
}
</style>
