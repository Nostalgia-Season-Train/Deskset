<script setup>
import { ref } from 'vue'

const battery_percent = ref(100)
const is_plug = ref(true)


/* === SSE === */
import { getServerInfo } from '../request'

const server = await getServerInfo()

// 绑定
import { EventSource } from 'eventsource'

const stream = new EventSource(`http://${ server.host }:${ server.port }/v0/device/stream`, {
  fetch: (input, init) =>
    fetch(input, {
      ...init,
      headers: {
        ...init.headers,
        Authorization: `Bearer ${ server.token }`
      }
    })
})

stream.addEventListener('message', (event) => {
  const info = JSON.parse(event.data)
  battery_percent.value = info.percent
  is_plug.value = info.plug
})

// 解绑
import { onBeforeUnmount } from 'vue'

onBeforeUnmount(() => stream.close())
</script>


<template>
<div style="display: flex; align-items: center;">
  <div class="battery">
    <div class="charging"></div>
  </div>
  <span class="num">{{ battery_percent }}%</span>
  <span class="text" v-if="is_plug">充电中</span>
</div>
</template>


<style scoped>
.battery {
  position: relative;  /* 帮助伪元素定位 */
  width: 60px;
  height: 25px;
  box-sizing: border-box;  /* 确保总宽总高为 60 * 25 */

  padding: 2.4px;

  border: 3px solid #FFF;
}
.battery::after {  /* 电池头 */
  position: absolute;
  width: 4px;
  height: 60%;

  content: '';
  background-color: #FFF;

  top: 50%;                     /* 相对父级下移 50% 左上垂直居中父级 */
  transform: translateY(-50%);  /* 相对自身上移 50% 中心垂直居中父级 */
  right: -10px;
}

.charging {
  width: v-bind(battery_percent + '%');
  height: 100%;
  background-color: white;
}

.num::before {
  content: '';
  display: inline-block;  /* 与百分比同一行撑开间距 */
  width: 20px;
}
.num {
  color: white;
  font-size: 36px;
}
.text::before {
  content: '';
  display: inline-block;
  width: 12px;
}
.text {
  color: #FFFA;
  font-size: 24px;
}
</style>
