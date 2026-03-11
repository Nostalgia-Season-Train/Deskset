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
      <div>
        <div>{{ day }}</div>
        <div>天</div>
      </div>
      <div>
        <div>{{ hour }}</div>
        <div>时</div>
      </div>
      <div>
        <div>{{ minute }}</div>
        <div>分</div>
      </div>
      <div>
        <div>{{ second }}</div>
        <div>秒</div>
      </div>
    </span>
  </div>

</div>
</template>


<style lang="less" scoped>
.countdown {
  box-sizing: border-box;
  width: 270px;
  height: 120px;

  color: #000;
  background: #FFF7;
  border: solid 1px #FFF;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .title {
    font-size: 24px;
  }
  .text-expired,
  .text-datetime {
    font-size: 20px;
  }
  .text-datetime {
    display: flex;
    gap: 10px;
    :nth-child(n) {
      width: 25px;
      text-align: center;
      :nth-child(1) {
        color: #000D;
        font-weight: 1000;
        text-align: center;
      }
    }
  }
}
</style>
