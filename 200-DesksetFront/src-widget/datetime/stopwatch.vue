<script lang="ts" setup>
import { Reactive, Ref } from 'vue'

class StopWatch {
  _start: number | null = null
  _isEnd: boolean = false  // step 判断结束的标志
  _time: Reactive<{ high: string, low: string }>
  _isTiming: Ref<boolean>

  constructor(time: Reactive<{ high: string, low: string }>, isTiming: Ref<boolean>) {
    this._time = time
    this._isTiming = isTiming
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
    if (this._start != null) {
      return  // start != null 正在计时
    }
    requestAnimationFrame(this._step)
    this._isTiming.value = true
  }

  finish = () => {
    this._isEnd = true
    this._isTiming.value = false
  }
}


import { ref, reactive, onBeforeUnmount } from 'vue'

const isTiming = ref(false)
const time = reactive({ high: '00:00.00', low: '' })
const stopwatch = new StopWatch(time, isTiming)

onBeforeUnmount(() => stopwatch.finish())  // 重要！step 不会自动停止


/* === 图标 === */
import { Play, Square } from 'lucide-vue-next'


/* === 配置 === */
const model = defineModel<{
  highcolor: string,
  lowcolor: string
}>({ required: true })
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
      >重置</span>
    </div>
    <div class="button">
      <span
        style="color: #FFF; font-weight: 300; background: #66BB6A;"
        v-if="!isTiming"
        @click="stopwatch.begin"
      >开始</span>
      <span
        style="color: #FFF; font-weight: 300; background: #E53935;"
        v-else
        @click="stopwatch.finish"
      >结束</span>
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
    span {
      padding: 5px 10px;
      border-radius: 5px;
    }
  }
}
</style>
