<script lang="ts" setup>
import { ref } from 'vue'
import { ElDatePickerPanel } from 'element-plus'
const value = ref(new Date())  // value 改变到其他月份，日期面板会自动跳转

import { ElConfigProvider } from 'element-plus'
import zh_cn from 'element-plus/es/locale/lang/zh-cn'
</script>


<template>
<div class="calendar">
  <ElConfigProvider :locale="zh_cn">
    <ElDatePickerPanel v-model="value"/>
  </ElConfigProvider>
</div>
</template>


<style lang="less" scoped>
:deep(.el-picker-panel) {
  width: fit-content;
  height: fit-content;
  background: transparent;
  border: solid 1px transparent;
  .el-picker-panel__body-wrapper {
    .el-picker-panel__body {
      .el-date-picker__header {
        display: none;
      }
      .el-picker-panel__content {
        margin: 3px;
        pointer-events: none;
        color: white;
        th {
          color: white;
        }
        .prev-month,
        .next-month {
          color: #FFF9;
        }
      }
    }
  }
}
</style>
