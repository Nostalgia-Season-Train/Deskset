<script lang="ts" setup>
import { ref } from 'vue'

const model = defineModel<{
  title: string,
  deadline: number
}>({ required: true })

const isExpire = ref(false)  // 到期标志

const day = ref(0)
const hour = ref(0)
const minute = ref(0)
const second = ref(0)

const updateCountdown = async () => {
  const datetimeNow = new Date().getTime()
  const datetimeDeadline = new Date(model.value.deadline).getTime()
  const remain = datetimeDeadline - datetimeNow

  if (remain <= 0) {
    return isExpire.value = true
  }
  isExpire.value = false

  day.value = Math.floor(remain / (1000 * 60 * 60 * 24))
  hour.value = Math.floor((remain / (1000 * 60 * 60)) % 24)
  minute.value = Math.floor((remain / (1000 * 60)) % 60)
  second.value = Math.floor((remain / 1000) % 60)
}


/* === 轮询 === */
import { useIntervalFn } from '@vueuse/core'

useIntervalFn(updateCountdown, 500)
</script>


<template>
<div class="countdown">

  <div class="title">{{ model.title }}</div>

  <div v-if="isExpire">
    <span class="text-expired">截止日期已到！</span>
  </div>
  <div v-else>
    <span class="text-datetime">
      {{ day }} 天 {{ hour }} 时 {{ minute }} 分 {{ second }} 秒
    </span>
  </div>

</div>
</template>
