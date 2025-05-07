<script lang="ts" setup>
const state = defineModel({ type: Boolean, required: true })  // false 关 true 开
</script>


<template>
<div class="container">
  <div class="switch" @click="state = !state">
    <span :class="`slide ${state ? 'active' : ''}`" ref="slide"></span>
  </div>
</div>
</template>


<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;

  --color: #64B5F6;
  --size: 20px;
  --len: 50px;
}

.switch {
  position: relative;
  width: var(--len);
  height: var(--size);
  cursor: pointer;
  // 发光效果，注意用的是 drop-shadow 而不是 box-shadow
  filter: drop-shadow(0 0 2px var(--color))
          drop-shadow(0 0 5px var(--color));

  // 边框
    // inset 相当于 padding，但是更加灵活
  &::before {
    content: '';
    position: absolute;
    inset: -4px;
    border: 1px solid var(--color);
  }

  // 滑块
  .slide {
    position: absolute;
    width: var(--size);
    height: var(--size);
    background: var(--color);
    pointer-events: none;  // 禁止文字选中
    transition: 0.2s ease-in-out;
  }
  .slide.active {
    transform: translateX(calc(var(--len) - var(--size)));
  }
}
</style>
