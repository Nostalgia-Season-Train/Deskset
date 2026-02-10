<script lang="ts" setup>
import { ref } from 'vue'
import { ElDatePickerPanel } from 'element-plus'
const value = ref(new Date())  // value 改变到其他月份，日期面板会自动跳转
</script>


<template>
<div class="calendar">
  <ElDatePickerPanel v-model="value"/>
</div>
</template>


<style lang="less" scoped>
:deep(.el-picker-panel) {
  .el-picker-panel__content {
    pointer-events: none;
  }
}
</style>
