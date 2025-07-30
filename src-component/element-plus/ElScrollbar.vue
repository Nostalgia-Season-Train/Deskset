<script lang="ts" setup>
import { ElScrollbar } from 'element-plus'
</script>


<template>
<el-scrollbar>
  <slot></slot>
</el-scrollbar>
</template>


<style lang="less" scoped>
:deep(.el-scrollbar__thumb) {
  display: none;  // 去掉滚动条
}
</style>
