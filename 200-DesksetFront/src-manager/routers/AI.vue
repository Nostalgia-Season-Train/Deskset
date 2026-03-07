<script lang="ts" setup>
/* ==== DesksetBack ==== */
import axios from 'axios'

const controller = new AbortController()
let key = -1

const sendMessage = async () => {
  const body = senderText.value
  senderText.value = ''

  // 用户消息
  key += 1
  list.value.push({
    key: key,
    role: 'user',
    placement: 'end',
    content: body,
    isMarkdown: true
  })

  // AI 消息
  key += 1
  list.value.push({
    key: key,
    role: 'ai',
    placement: 'start',
    content: '',
    isMarkdown: true
  })
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
            list.value[key].content += obj.delta
          if (obj.type === 'response.output_item.done' && obj.item.type === 'message') {
            list.value[key].content = ''
            for (const content of obj.item.content)
              // 注 1：```xml 结尾是因为 AI 后面调用了 MCP 工具，不是 BUG
              list.value[key].content += content.text + '\n'
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
import type {
  BubbleListItemProps,
  BubbleListProps
} from 'vue-element-plus-x/types/BubbleList'

type listType = BubbleListItemProps & {
  key: number
  role: 'user' | 'ai'
}


import { ref } from 'vue'
import {
  BubbleList,
  Sender
} from 'vue-element-plus-x'

const senderText = ref('')
const list = ref<BubbleListProps<listType>['list']>([])


const getLatestMessages = async () => {
  const response = await axios.get('/ai/latest-messages')
  for (const message of response.data) {
    if (message?.role === 'user') {
      key += 1
      list.value.push({
        key: key,
        role: 'user',
        placement: 'end',
        content: message.content,
        isMarkdown: true
      })
    }
    if (message?.role === 'assistant') {
      key += 1
      list.value.push({
        key: key,
        role: 'ai',
        placement: 'start',
        content: message.content,
        isMarkdown: true
      })
    }
  }
}
getLatestMessages()


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

  <!-- @click.prevent：禁用链接跳转 -->
  <BubbleList :list="list" style="user-select: text;" @click.prevent/>

  <Sender v-model="senderText" :auto-size="{ minRows: 3, maxRows: 5 }" @keydown.enter="sendMessage">
    <template #action-list>
      <ElButton :disabled="senderText === ''" @click="sendMessage">
        <ElIcon><Promotion/></ElIcon>
      </ElButton>
    </template>
  </Sender>

</ElScrollbar>
</template>
