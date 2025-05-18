<script lang="ts" setup>
import { ref } from 'vue'

const percent = ref<number>(50)
</script>


<template>
<div class="progress-container">
  <div class="progress">
    <span class="percent" :style="`width: ${percent}%;`">{{ percent }}</span>
  </div>
</div>
</template>


<style lang="less" scoped>
.progress-container {
  .progress {
    box-sizing: border-box;
    width: 200px;
    height: 12px;

    display: flex;
    justify-content: left;
    align-items: center;

    background: #333;
    border: 1px solid #FFF;

    .percent {
      width: 0;
      height: 100%;

      display: flex;
      justify-content: center;
      align-items: center;

      font-size: 14px;
      color: #000;
      background: #FFF;
    }
  }
}
</style>
