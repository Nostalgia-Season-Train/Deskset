<script lang="ts" setup>
const helloworld = async () => {
  return 'helloworld'
}


/* ==== BroadcastDesktopServer ==== */
  // 将 Broadcast 由事件/消息改成请求/响应模型
import { onMounted, onUnmounted } from 'vue'

const actions = { helloworld }
const broadcast = new BroadcastChannel('Desktop')
const onReceive = async (msg: MessageEvent) => {
  const request = JSON.parse(msg.data)

  let result, error
  try {
    result = await (actions as any)[request.funcName](...request.funcArgs)
  } catch (err) {
    error = err
  }

  broadcast.postMessage(
    JSON.stringify({
      id: request.id,
      result: result,
      error: error
    })
  )
}

onMounted(() => broadcast.onmessage = onReceive)
onUnmounted(() => broadcast.onmessage = null)
</script>



<template>
</template>



<style scoped>
</style>
