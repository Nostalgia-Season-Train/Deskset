<script lang="ts" setup>
import { Ref } from 'vue'

class StopWatch {
  _start: number | null = null
  _isEnd: boolean = false  // step 判断结束的标志
  _timeRef: Ref

  constructor(timeRef: Ref) {
    this._timeRef = timeRef
  }

  // step 传入 requestAnimationFrame 轮询回调自身
  _step = (timestamp: number) => {
    if (this._isEnd == true) {
      this._start = null
      this._isEnd = false
      return
    }

    if (this._start == null) {
      this._start = timestamp
    }
    const elapsed = timestamp - this._start
    this._timeRef.value = this._msFormat(elapsed)

    requestAnimationFrame(this._step)
  }

  // 毫秒 ms 转为 分:秒:十毫秒
  _msFormat = (ms: number): string => {
    const min = Math.floor(ms / 60000)           // 1 min = 60000 ms
    const sec = Math.floor((ms % 60000) / 1000)  // 1 sec = 1000 ms
    const tensms = Math.floor((ms % 1000) / 10)  // 10 ms

    return [min, sec, tensms].map(n => String(n).padStart(2, '0')).join(':')
  }

  begin = () => {
    if (this._start != null) {
      return  // start != null 正在计时
    }
    requestAnimationFrame(this._step)
  }

  finish = () => {
    this._isEnd = true
  }
}


import { ref, onBeforeUnmount } from 'vue'

const isTiming = ref(false)
const time = ref('00:00:00')
const stopwatch = new StopWatch(time)

onBeforeUnmount(() => stopwatch.finish())  // 重要！step 不会自动停止


/* === 图标 === */
import { Play, Square } from 'lucide-vue-next'
</script>


<template>
<div class="container">
  <div class="time">{{ time }}</div>
  <div class="button">
    <div v-if="isTiming == false" @click="stopwatch.begin(); isTiming = true">
      <Play/>
    </div>
    <div v-if="isTiming == true" @click="stopwatch.finish(); isTiming = false">
      <Square/>
    </div>
  </div>
</div>
</template>


<style lang="less" scoped>
.container {
  width: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;  // time 变化会左右移动，后面优化
  color: white;
  .time {
    font-size: 1.8em;
  }
  .button {
    font-size: 1.2em;
    transition: all .1s ease-out;
    &:active {
      transform: translateY(5px);
    }
  }
}
</style>
