<script lang="ts" setup>
import { Reactive, Ref } from 'vue'

class StopWatch {
  _elapsed: number = 0
  _lastTimestamp: number | null = null
  _time: Reactive<{ high: string, low: string }>
  _status: Ref<'idle' | 'running' | 'paused'>  // 空闲 > 运行 > 暂停

  constructor(time: Reactive<{ high: string, low: string }>, status: Ref<'idle' | 'running' | 'paused'>) {
    this._time = time
    this._status = status
  }

  // step 传入 requestAnimationFrame 轮询回调自身
  _step = (timestamp: number) => {
    if (this._status.value !== 'running') {
      return  // 非运行状态，直接退出
    }

    this._lastTimestamp = this._lastTimestamp ?? timestamp
    this._elapsed += timestamp - this._lastTimestamp
    this._lastTimestamp = timestamp
    const { high, low } = this._msFormat(this._elapsed)
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
    const fulltime = `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}.${tensms.toString().padStart(2, '0')}`

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
    if (this._status.value !== 'idle') {
      return
    }
    this._status.value = 'running'
    this._lastTimestamp = null
    requestAnimationFrame(this._step)
  }

  togglePause = () => {
    if (this._status.value === 'paused') {
      this._status.value = 'running'
      this._lastTimestamp = null
      requestAnimationFrame(this._step)
    } else {
      this._status.value = 'paused'
    }
  }

  finish = () => {
    this._status.value = 'idle'
    this._elapsed = 0
    this._lastTimestamp = null
    this._time.high = '00:00.00'
    this._time.low = ''
  }
}


import { ref, reactive, onBeforeUnmount } from 'vue'

const status = ref<'idle' | 'running' | 'paused'>('idle')
const time = reactive({ high: '00:00.00', low: '' })
const stopwatch = new StopWatch(time, status)

onBeforeUnmount(() => stopwatch.finish())  // 重要！step 不会自动停止
</script>


<template>
<div class="container">

  <div class="time">
    <span>{{ time.high }}</span>
    <span>{{ time.low }}</span>
  </div>

  <div class="second">
    <div class="button">
      <span
        style="color: #FFF; font-weight: 300; background: #2196F3;"
        @click="stopwatch.finish"
      >重置</span>
    </div>
    <div class="button">
      <span
        style="color: #FFF; font-weight: 300; background: #66BB6A;"
        v-if="status === 'idle'"
        @click="stopwatch.begin"
      >开始</span>
      <span
        style="color: #FFF; font-weight: 300; background: #E53935;"
        v-if="status === 'running'"
        @click="stopwatch.togglePause"
      >暂停</span>
      <span
        style="color: #FFF; font-weight: 300; background: #FFB300;"
        v-if="status === 'paused'"
        @click="stopwatch.togglePause"
      >继续</span>
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
* {
  font-family: 'MisansVF';
}

.container {
  padding: 5px 15px;
  padding-bottom: 15px;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;

  color: #000C;
  background: #FFFD;
  border: solid 1px #FFF;
  border-radius: 5px;
  box-shadow: 0 2px 4px #0003;

  .time {
    font-size: 32px;
    font-weight: 400;
    font-feature-settings: 'ss01', 'tnum';
  }
  // .button {
  //   position: relative;
  //   top: 1px;
  //   font-size: 1.2em;
  //   transition: all .1s ease-out;
  //   &:active {
  //     transform: translateY(5px);
  //   }
  // }

  .second {
    display: flex;
    justify-content: space-between;
    gap: 27px;
    .button {
      transition: all .1s ease-out;
      &:active {
        transform: translateY(5px);
      }
      span {
        padding: 5px 10px;
        border-radius: 5px;
      }
    }
  }
}
</style>
