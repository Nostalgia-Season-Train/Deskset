<script lang="ts" setup>
import { ElScrollbar } from 'element-plus'
</script>


<template>
<el-scrollbar>
  <!-- 已知错误：滚动条隐藏后，点击原先所在位置（一般位于右边），会使页面跳转到顶部 -->
  <slot></slot>
</el-scrollbar>
</template>


<style lang="less" scoped>
:deep(.el-scrollbar__thumb) {
  display: none;  // 去掉滚动条
}
</style>
