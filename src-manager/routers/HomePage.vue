<script lang="ts" setup>
import { inject, onUnmounted } from 'vue'
import { AxiosStatic } from 'axios'

const axios = inject('$axios') as AxiosStatic
const controller = new AbortController()

const refresh = async () => {
  axios.get('/v0/note/obsidian-manager/noteapi/event', {
    adapter: 'fetch',
    responseType: 'stream',
    signal: controller.signal
  })
  .then(response => {
    const reader = response.data.getReader()
    const decoder = new TextDecoder()

    reader.read().then(function process({ done, value }) {
      // 1、是否传输结束
      if (done) {
        return reader.read().then(refresh)
      }

      // 2、解析数据
      const chunk = decoder.decode(value, { stream: true })
      console.log(chunk)

      // 3、回调自身
      return reader.read().then(process)
    })
    .catch(error => console.log('fetch catch', error))
  })
  .catch(error => console.log('axios catch', error))
}
refresh()

// controller.abort('caught by axios')
onUnmounted(() => {
  controller.abort('caught by fetch')
})
</script>


<template>
</template>


<style lang="less" scoped>
</style>
