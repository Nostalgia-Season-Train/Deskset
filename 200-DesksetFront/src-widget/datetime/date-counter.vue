<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

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
    <div class="text-expired">截止日期已到！</div>
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

  <div class="deadline">截止日期：{{ dayjs(model.deadline).format('MM/DD HH:mm') }}</div>

</div>
</template>


<style lang="less" scoped>
@import '../style.less';

* {
  font-family: 'MisansVF';
}

.countdown {
  box-sizing: border-box;
  width: 200px;
  height: fit-content;

  .dsw-box();
  background: #FFF;
  border: none;

  &>* {
    box-sizing: border-box;
    width: 100%;
    padding: 5px 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .title {
    .dsw-text();
    color: #FFF;
    font-size: 18px;
    font-weight: 300;
    background: #42A5F5;
  }
  .text-expired,
  .text-datetime {
    .dsw-text();
    font-size: 18px;
  }
  .text-datetime {
    display: flex;
    gap: 10px;
    :nth-child(n) {
      width: 25px;
      text-align: center;
      :nth-child(1) {
        .dsw-text-title();
      }
    }
  }
  .deadline {
    .dsw-text();
    color: #111;
    background: #E9E9E9;
  }
}
</style>
