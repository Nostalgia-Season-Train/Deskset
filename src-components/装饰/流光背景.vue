<script lang="ts" setup>
import { ref } from 'vue'

const x = ref(0)
const y = ref(0)

const setLightPos = async (e: MouseEvent) => {
  x.value = e.offsetX
  y.value = e.offsetY
}
</script>


<template>
<div>
  <div @mousemove="setLightPos" class="stream-light">
    <span>流光</span>
  </div>
</div>
</template>


<style scoped>
.stream-light {
  --light-color: #FFCA28;  /* Amber 400 */
}

.stream-light {
  position: relative;
  padding: 20px 60px;
  background-color: rgba(45,45,45,1);
  border-radius: 50px;
  color: #999;
  font-size: 1.5em;
  text-decoration: none;
  overflow: hidden;  /* 隐藏溢出的流光 */
  transition: .5s;  /* 文字发光过渡 */
}

/* 流光：鼠标移入前隐藏 */
.stream-light::before {
  content: '';
  position: absolute;
  left: v-bind(x + 'px');
  top: v-bind(y + 'px');
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  background: radial-gradient(var(--light-color), transparent, transparent);
  opacity: 0;
  transition: .5s, top 0s, left 0s;  /* left, top 禁用过渡，否则移动不平滑 */
}

/* 滤镜 */
.stream-light::after {
  content: '';
  background-color: rgba(45,45,45,.8);
  position: absolute;
  inset: 2px;  /* 边框发光 */
  border-radius: 48px;
}
.stream-light>span {
  position: relative;
  z-index: 1;  /* 文字在滤镜上显示 */
  letter-spacing: .2em;  /* 字符间距 */
}

/* 鼠标移入：显示流光 + 文字发光 */
.stream-light:hover::before {
  opacity: 1;
}
.stream-light:hover {  /* 不能加 span，不然发光没有渐变效果 transition: 0.5s */
  color: var(--light-color);
  text-shadow: 0 0 15px var(--light-color),
               0 0 40px var(--light-color);
}
</style>
