<script setup>
import { ref } from 'vue'
import axios from 'axios'

const greeting = ref('')  // 空字符串，避免第一次刷掉时产生闪烁

const greet = async () => {
  const repGreeting = (await axios.get('/v0/greet/simple')).data.result.greeting
  greeting.value = ''
  for (const [index, char] of Array.from(repGreeting).entries()) {
    setTimeout(() => { greeting.value += char }, 250 * index)  // 首个字符不会延迟出现，因为 index 从 0 开始
  }
}
greet()


import { useIntervalFn } from '@vueuse/core'

useIntervalFn(greet, 30 * 1000)
</script>


<template>
  <div class="greet">
    <span class="greeting">{{ greeting }}</span>
  </div>
</template>


<style lang="less" scoped>
.greet {
  color: white;
  font-size: 20px;
  white-space: nowrap;
}
</style>
