<script lang="ts" setup>
import { onUnmounted } from 'vue'
import axios from 'axios'

const controller = new AbortController()

const refresh = async () => {
  try {
    const response = await axios.get('/v0/note/obsidian/is_online', {
      adapter: 'fetch',
      responseType: 'stream',
      signal: controller.signal
    })
    const reader = response.data.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value)
      console.log(chunk)
    }
  } catch { }
}
refresh()

onUnmounted(() => {
  controller.abort('caught by fetch')
})


/* === 子页面 === */
import DesktopInfo from './HomePage/DesktopInfo.vue'
import Sidebar from './HomePage/Sidebar.vue'
</script>


<template>
<div class="content">
  <DesktopInfo/>
  <Sidebar/>
</div>
</template>


<style lang="less" scoped>
.content {
  padding: 0 var(--content-padding);
  padding-bottom: var(--content-padding);
}
</style>
