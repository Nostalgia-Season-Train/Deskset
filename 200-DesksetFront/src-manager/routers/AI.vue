<script lang="ts" setup>
/* ==== DesksetBack ==== */
import axios from 'axios'
const controller = new AbortController()
const send = async () => {
  const body = senderText.value
  senderText.value = ''
  try {
    const response = await axios.post('/ai/hello', body, {
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
      for (const objtext of chunk.split('\n')) {
        if (objtext === '') continue
        try {
          const obj = JSON.parse(objtext)
          if (obj.type === 'response.output_text.delta')
            markdownText.value += obj.delta
          if (obj.type === 'response.output_item.done' && obj.item.type === 'message') {
            markdownText.value = ''
            for (const content of obj.item.content)
              // 注 1：```xml 结尾是因为 AI 后面调用了 MCP 工具，不是 BUG
              markdownText.value += content.text + '\n'
          }
        } catch { }
      }
    }
  } catch (error) {
    console.error('Stream processing error:', error)
  }
}

import { onUnmounted } from 'vue'
onUnmounted(() => {
  controller.abort('caught by fetch')
})


/* ==== Element Plus X ==== */
import { ref } from 'vue'
import {
  Bubble,
  Sender
} from 'vue-element-plus-x'

const markdownText = ref('')
const senderText = ref('')


/* ==== Element Plus ==== */
import {
  ElScrollbar,
  ElButton,
  ElIcon
} from 'element-plus'
import { Promotion } from '@element-plus/icons-vue'
</script>


<template>
<ElScrollbar>

  <Bubble :content="markdownText" placement="start"/>

  <Sender v-model="senderText" :auto-size="{ minRows: 3, maxRows: 5 }">
    <template #action-list>
      <ElButton @click="send" :disabled="senderText === ''">
        <ElIcon><Promotion/></ElIcon>
      </ElButton>
    </template>
  </Sender>

</ElScrollbar>
</template>
