<script setup>
import { ref } from "vue"
import { getDesksetReq } from '../request'

const greeting = ref("简单问候")

const greet = async () => {
  const desksetReq = await getDesksetReq()
  const repGreeting = (await desksetReq.get('/v0/greet/simple')).data.data.greeting
  greeting.value = ''
  for (const [index, char] of Array.from(repGreeting).entries()) {
    setTimeout(() => { greeting.value += char }, 250 * index)  // 首个字符不会延迟出现，因为 index 从 0 开始
  }
}
greet()


import { useIntervalFn } from "@vueuse/core"

useIntervalFn(greet, 60000)
</script>


<template>
  <div class="greet">
    <span class="greeting">{{ greeting }}</span>
  </div>
</template>


<style lang="less" scoped>
.greet {
  color: white;
  font-size: 24px;
}
</style>
