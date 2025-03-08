<script setup>
import { ref } from "vue"
import { desksetReq } from '../request'

const year  = ref("2024")
const month = ref("12")
const day   = ref("24")
const week  = ref("星期天")

const date = async () => {
  const response_date = await desksetReq.get('/v0/datetime/date')
  year.value = response_date.data.data.year
  month.value = response_date.data.data.month
  day.value = response_date.data.data.day

  const response_week = await desksetReq.get('/v0/datetime/week')
  week.value = response_week.data.data.week
}
date()


import { useIntervalFn } from '@vueuse/core'

useIntervalFn(date, 1000)
</script>


<template>
  <div class="date">
    <span class="year-month-day">{{ year }} 年 {{ month }} 月 {{ day }} 日</span>
    <span class="split"> - </span>
    <span class="week">{{ week }}</span>
  </div>
</template>


<style scoped>
.date {
  color: white;
}

.year-month-day {
  font-size: 24px;
}

.split, .week {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
}
</style>
