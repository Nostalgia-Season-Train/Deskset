<script lang="ts" setup>
/* ==== DesksetBack ==== */
import axios from 'axios'
const controller = new AbortController()
const refresh = async () => {
  try {
    const response = await axios.get('/ai/hello', {
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
          if (obj.type === 'response.output_item.done') {
            markdownText.value = ''
            for (const content of obj.item.content)
              markdownText.value += content.text + '\n'
          }
        } catch { }
      }
    }
  } catch (error) {
    console.error('Stream processing error:', error)
  }
}
refresh()

import { onUnmounted } from 'vue'
onUnmounted(() => {
  controller.abort('caught by fetch')
})


/* ==== Element Plus X ==== */
import { ref } from 'vue'
import { Bubble } from 'vue-element-plus-x'

const markdownText = ref('')


/* ==== Element Plus ==== */
import { ElScrollbar } from 'element-plus'
</script>


<template>
<ElScrollbar>

  <Bubble :content="markdownText" placement="start"/>

</ElScrollbar>
</template>
