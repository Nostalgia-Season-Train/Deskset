<script lang="ts" setup>
import { reactive } from 'vue'
import dayjs from 'dayjs'

const time = reactive({
  hour: '00',
  minute: '00',
  dayofweek: 'Sunday',
  dayofmonth: '1',
  month: 'January'
})

const refresh = async () => {
  const now = dayjs()
  time.hour = now.format('HH')
  time.minute = now.format('mm')
  time.dayofweek = now.format('dddd')
  time.dayofmonth = now.format('D')
  time.month = now.format('MMMM')
}


/* === 轮询 === */
import { useIntervalFn } from '@vueuse/core'

// 1、await 以便 onErrorCaptured 接住错误
// 2、不要用 onMounted，会使 useIntervalFn 自动清理失效
useIntervalFn(refresh, 250)
</script>


<template>
  <div class="clock">
    <div class="time">{{ time.hour }}:{{ time.minute }}</div>
    <div class="date">{{ time.dayofweek }}, {{ time.dayofmonth }} {{ time.month }}</div>
  </div>
</template>


<style lang="less" scoped>
.clock {
  display: flex;
  flex-direction: column;
  align-items: center;

  * {
    font-family: 'Aleo';
  }
  .time {
    height: 95px;  // 缩减行高空白
    color: #FFFE;
    font-size: 84px;
  }
  .date {
    color: #FFFA;
    font-size: 20px;
  }
}
</style>
