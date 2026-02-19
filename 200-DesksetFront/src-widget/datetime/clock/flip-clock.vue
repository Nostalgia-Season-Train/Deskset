<script lang="ts" setup>
import { onMounted, onBeforeUnmount, useTemplateRef } from 'vue'
import dayjs from 'dayjs'

const ref_hour_tens = useTemplateRef('data-hour-tens')
const ref_hour_ones = useTemplateRef('data-hour-ones')
const ref_min_tens = useTemplateRef('data-min-tens')
const ref_min_ones = useTemplateRef('data-min-ones')
const ref_sec_tens = useTemplateRef('data-sec-tens')
const ref_sec_ones = useTemplateRef('data-sec-ones')

/* === 挂载后才能用 querySelector 匹配网页元素 === */
onMounted(() => {
  const hour_tens = ref_hour_tens.value
  const hour_ones = ref_hour_ones.value
  const min_tens = ref_min_tens.value
  const min_ones = ref_min_ones.value
  const sec_tens = ref_sec_tens.value
  const sec_ones = ref_sec_ones.value
  if (hour_tens == null) return
  if (hour_ones == null) return
  if (min_tens == null) return
  if (min_ones == null) return
  if (sec_tens == null) return
  if (sec_ones == null) return

  // DataVue：组件作用域 style scoped 创建的 data-v 属性
  const getDataVueAttribute = (element: Element) => {
    for (const attribute of element.getAttributeNames()) {
      if (attribute.startsWith('data-v')) return attribute
    }
  }
  const dataVue = getDataVueAttribute(sec_ones)
  if (dataVue == null) return

  const refresh = setInterval(async () => {
    const time = dayjs().format('HHmmss')
    flip(hour_tens, time[0], dataVue)
    flip(hour_ones, time[1], dataVue)
    flip(min_tens, time[2], dataVue)
    flip(min_ones, time[3], dataVue)
    flip(sec_tens, time[4], dataVue)
    flip(sec_ones, time[5], dataVue)
  }, 500)
  onBeforeUnmount(() => clearInterval(refresh))

  const flip = async (flipCard: Element, newNum: string, dataVue: string) => {
    const topHalf = flipCard.querySelector('.top')
    const bottomHalf = flipCard.querySelector('.bottom')
    if (topHalf == null || bottomHalf == null || topHalf.textContent == null) return

    const oldNum = topHalf.textContent
    if (newNum === oldNum) return

    // setAttribute(dataVue, '') 添加对应 data-v 属性，让 style scoped 中的 CSS 生效
    const topFlip = document.createElement('div')
    topFlip.classList.add('top-flip')
    topFlip.setAttribute(dataVue, '')
    const bottomFlip = document.createElement('div')
    bottomFlip.classList.add('bottom-flip')
    bottomFlip.setAttribute(dataVue, '')

    // 翻转时，topHalf、bottomFlip 视作新面，topFlip、bottomHalf 视作旧面
    topFlip.textContent = oldNum
    topFlip.addEventListener('animationstart', () => topHalf.textContent = newNum)
    topFlip.addEventListener('animationend', () => topFlip.remove())
    bottomFlip.textContent = newNum
    bottomFlip.addEventListener('animationend', () => {
      bottomHalf.textContent = newNum
      bottomFlip.remove()
    })

    // 插入动画元素 Flip，开始翻转
    flipCard.append(topFlip, bottomFlip)
  }
})
</script>


<template>
<div class="container">
  <div class="segment">
    <div class="flip-card" ref="data-hour-tens">
      <div class="top">0</div>
      <div class="bottom">0</div>
    </div>
    <div class="flip-card" ref="data-hour-ones">
      <div class="top">0</div>
      <div class="bottom">0</div>
    </div>
  </div>
  <div class="segment">
    <div class="flip-card" ref="data-min-tens">
      <div class="top">0</div>
      <div class="bottom">0</div>
    </div>
    <div class="flip-card" ref="data-min-ones">
      <div class="top">0</div>
      <div class="bottom">0</div>
    </div>
  </div>
  <div class="segment">
    <div class="flip-card" ref="data-sec-tens">
      <div class="top">0</div>
      <div class="bottom">0</div>
    </div>
    <div class="flip-card" ref="data-sec-ones">
      <div class="top">0</div>
      <div class="bottom">0</div>
    </div>
  </div>
</div>
</template>


<style lang="less" scoped>
.container {
  width: 480px;  // 固定宽度，否则桌面边缘将会挤压元素布局
  display: flex;
  justify-content: space-between;
  // gap: 50px;  // 时、分、秒间距（目前采用 space-between 自然调整间距）

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
}

.segment {
  display: flex;
  gap: 5px;  // 十位、个位间距

  .flip-card {
    position: relative;
    display: inline-flex;
    flex-direction: column;

    .top, .bottom, .top-flip, .bottom-flip {
      height: .75em;
      line-height: 1;
      padding: .25em;
      overflow: hidden;
    }

    .bottom, .bottom-flip {
      display: flex;
      align-items: flex-end;
    }

    div {
      color: #E0E0E0;
      // 字体大小，间接调整卡片大小
        // 不建议带小数点，卡片翻页使分界线移位
      font-size: 60px;
    }
    // 上半部分边框背景
    .top, .top-flip {
      border-radius: .07em .07em 0 0;
    }
    // 下半部分边框背景
    .bottom, .bottom-flip {
      border-radius: 0 0 .07em .07em;
    }
  }
}

.top-flip {
  position: absolute;
  width: 100%;
  animation: flip-top 250ms ease-in;
  transform-origin: bottom;
}
@keyframes flip-top {
  100% { transform: rotateX(90deg); }
}
.bottom-flip {
  position: absolute;
  bottom: 0;
  width: 100%;
  animation: flip-bottom 250ms ease-in 250ms;
  transform-origin: top;
  transform: rotateX(90deg);
}
@keyframes flip-bottom {
  100% { transform: rotateX(0deg); }
}

.top, .top-flip {
  background-color: #212121;
}
.bottom, .bottom-flip {
  background-color: #757575;
}
</style>
