<script setup>
import { ref } from "vue"
import { desksetReq } from '../request'

const hour   = ref("00")
const minute = ref("00")
const ampm   = ref("am")

const time = async () => {
  const response = await desksetReq.get('/v0/datetime/time12')
  hour.value = response.data.data.hour
  minute.value = response.data.data.minute
  ampm.value = response.data.data.ampm
}
time()


import { useIntervalFn } from "@vueuse/core"

useIntervalFn(time, 250)
</script>


<template>
  <div class="time">
    <span class="hour-minute">{{ hour }}:{{ minute }}</span>
    <span class="ampm">{{ ampm }}</span>
  </div>
</template>


<style scoped>
.time {
  color: white;
}

.time>.hour-minute {
  font-size: 68px;
}

.time>.ampm {
  font-size: 54px;
}
</style>
