<script lang="ts" setup>
import { Reactive } from 'vue'

class StopWatch {
  _start: number | null = null
  _isEnd: boolean = false  // step 判断结束的标志
  _time: Reactive<{ high: string, low: string }>

  constructor(time: Reactive<{ high: string, low: string }>) {
    this._time = time
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
    const { high, low } = this._msFormat(elapsed)
    this._time.high = high
    this._time.low = low

    requestAnimationFrame(this._step)
  }

  // 毫秒 ms 转为 分:秒:十毫秒
  _msFormat = (ms: number) => {
    // 加快动画速度：ms *= 10；减慢动画速度：ms /= 10
    const min = Math.floor(ms / 60000)           // 1 min = 60000 ms
    const sec = Math.floor((ms % 60000) / 1000)  // 1 sec = 1000 ms
    const tensms = Math.floor((ms % 1000) / 10)  // 10 ms

    const digitNumber = String(min * 10000 + sec * 100 + tensms).length  // 位数 = 数字个数
    const fulltime = [min, sec, tensms].map(n => String(n).padStart(2, '0')).join(':')

    if (digitNumber <= 2) {
      return {
        high: fulltime.slice(0, - digitNumber),
        low: fulltime.slice(- digitNumber)
      }
    } else if (2 < digitNumber && digitNumber <= 4) {
      return {
        high: fulltime.slice(0, - (digitNumber + 1)),
        low: fulltime.slice(- (digitNumber + 1))
      }
    } else {
      return {
        high: fulltime.slice(0, - (digitNumber + 2)),
        low: fulltime.slice(- (digitNumber + 2))
      }
    }
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


import { ref, reactive, onBeforeUnmount } from 'vue'

const isTiming = ref(false)
const time = reactive({ high: '00:00:00', low: '' })
const stopwatch = new StopWatch(time)

onBeforeUnmount(() => stopwatch.finish())  // 重要！step 不会自动停止


/* === 图标 === */
import { Play, Square } from 'lucide-vue-next'
</script>


<template>
<div class="container">
  <div class="time">
    <span>{{ time.high }}</span>
    <span style="color: #4FC3F7;">{{ time.low }}</span>
  </div>
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

  background: #FFF2;
  border: solid 1px #FFF8;

  .time {
    font-size: 1.8em;
    width: 121px;  // 固定宽度，避免数字变化（每个数字宽度不一样）带动位置变化
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
