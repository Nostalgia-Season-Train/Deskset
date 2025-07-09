<script setup>
import { reactive, inject } from 'vue'

const time = reactive({ hour: '00', minute: '00' })
const axios = inject('$axios')
const refresh = async () => {
  const result = (await axios.get('/v0/datetime/time')).data.result
  time.hour = result.hour
  time.minute = result.minute
}


/* === 轮询 === */
import { useIntervalFn } from '@vueuse/core'

// 1、await 以便 onErrorCaptured 接住错误
// 2、不要用 onMounted，会使 useIntervalFn 自动清理失效
await refresh()
useIntervalFn(refresh, 250)
</script>


<template>
  <div class="time">
    <span class="hour-minute">{{ time.hour }}:{{ time.minute }}</span>
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
