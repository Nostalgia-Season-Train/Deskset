<script setup>
import { ref } from "vue"
import { desksetReq } from '../request'

const greeting = ref("简单问候")

const greet = async () => {
  const response = await desksetReq.get('/v0/greet/simple')
  greeting.value = response.data.data.greeting
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


<style scoped>
.greet {
  color: white;
  font-size: 16px;
}
</style>
