<script lang="ts" setup>
withDefaults(defineProps<{
  size?: number,
  len?: number
}>(), {
  size: 21,
  len: 42
})
const state = defineModel<boolean>({ required: true })
</script>


<template>
<div class="container">
  <div class="switch">
    <span :class="`slide ${state ? 'active' : ''}`" ref="slide"></span>
  </div>
</div>
</template>


<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;

  --color: #FFF;
  // - [ ] 已知问题：--size: 26px 不能对齐滑块位置（偏左上方）
  --size: 27px;  // 比 Button 少 1px，视觉更加平衡
  --len: 56px;
}

.switch {
  position: relative;
  width: var(--len);
  height: var(--size);
  cursor: pointer;

  // 边框
    // inset 相当于 padding，但是更加灵活
    // 用伪元素不占用空间
  &::before {
    content: '';
    position: absolute;
    inset: 0px;
    border: 1px solid rgba(from var(--color) r g b / .3);
    transition: .3s ease;
  }
  &:hover::before {
    box-shadow: 0 0 5px 0 rgba(from var(--color) r g b / .1);
    border-color: rgba(from var(--color) r g b / .5);
  }

  // 滑块
  .slide {
    position: absolute;
    width: var(--size);
    height: var(--size);
    pointer-events: none;  // 禁止文字选中

    top: 0.1px;  // 原理未知，会降低滑块高度，从而正好垂直居中（否则偏上）
    padding: 3px;
    background: rgba(from var(--color) r g b / .3) content-box;

    transition: 0.2s ease-in-out;
    &.active {
      transform: translateX(calc(var(--len) - var(--size)));
      background: rgba(from var(--color) r g b / .9) content-box;
    }
  }
}
</style>

<style scoped>
* {
  --size: v-bind(size + 'px');
  --len: v-bind(len + 'px');
}
</style>
