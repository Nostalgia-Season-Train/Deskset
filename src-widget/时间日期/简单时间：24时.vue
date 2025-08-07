<script lang="ts" setup>
import { reactive } from 'vue'
import dayjs from 'dayjs'

const time = reactive({ hour: '00', minute: '00' })
const refresh = async () => {
  const now = dayjs()
  time.hour = now.format('HH')
  time.minute = now.format('mm')
}


/* === 轮询 === */
import { useIntervalFn } from '@vueuse/core'

// 1、await 以便 onErrorCaptured 接住错误
// 2、不要用 onMounted，会使 useIntervalFn 自动清理失效
useIntervalFn(refresh, 250)
</script>


<template>
  <div class="time">
    <span class="hour-minute">{{ time.hour }}:{{ time.minute }}</span>
  </div>
</template>


<style lang="less" scoped>
.time {
  // 限制空白区域，最大高度 80px
  height: 80px;
  display: flex;
  align-items: center;
  overflow: hidden;

  color: white;
}

.time>.hour-minute {
  font-size: 80px;
}
</style>
