<!-- 代码参考：https://www.bilibili.com/video/BV1d44y1N7hq -->

<template>
<div>
  <!-- 晴天 -->
  <div class="sunny">
    <div class="sun">
      <div class="rays"></div>
    </div>
  </div>
  <!-- 雨天 -->
  <div class="rainy">
    <div class="cloud"></div>
    <div class="rain"></div>
  </div>
  <!-- 多云 -->
  <div class="cloudy">
    <div class="cloud"></div>
    <div class="cloud"></div>
  </div>
</div>
</template>


<style scoped>
.sunny {
  /* :root 对子元素无效 */
  --sl: 50px;  /* sunny length 正方形边长 */

  position: relative;
  width: var(--sl);
  height: var(--sl);

  display: flex;
  justify-content: center;
  align-items: center;
}
.sunny .sun {
  width: calc(var(--sl) * 0.4);
  height: calc(var(--sl) * 0.4);

  box-shadow: 0 0 0 calc(var(--sl) * 0.06) orange;
  border-radius: 50%;

  animation: sunny 10s linear infinite;
}
.sunny .sun .rays {
  position: absolute;
  top: calc(var(--sl) * -0.32);  /* 调整使旋转居中，注意负号 */
  left: 50%;
  transform: translateX(-50%);

  width: calc(var(--sl) * 0.06);
  height: calc(var(--sl) * 0.18);

  background-color: yellow;
  box-shadow: 0 calc(var(--sl) * 0.86) yellow;  /* 另一条对称线 */
  border-radius: 4px;
}
.sunny .sun .rays::before,
.sunny .sun .rays::after {
  position: absolute;
  content: "";
  top: 0;
  left: 0;

  width: calc(var(--sl) * 0.06);
  height: calc(var(--sl) * 0.18);

  background-color: yellow;
  box-shadow: 0 calc(var(--sl) * 0.86) yellow;
  border-radius: 4px;

  transform: rotate(60deg);
  transform-origin: 50% calc(var(--sl) * 0.52);
}
.sunny .sun .rays::before {
  transform: rotate(-60deg);
}
@keyframes sunny {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
