<script lang="ts" setup>
import { ElMenu, ElMenuItem } from 'element-plus'

const emit = defineEmits(['jumpPage'])

const handleSelect = async (index: string) => { emit('jumpPage', index) }
</script>


<template>
<el-menu
  default-active="welcome"
  mode="horizontal"
  @select="handleSelect"
  :ellipsis="false"
>
  <el-menu-item index="welcome">
    <span>欢迎</span>
  </el-menu-item>
  <el-menu-item index="support">
    <span>支持</span>
  </el-menu-item>
  <el-menu-item index="float">
    <span>浮动</span>
  </el-menu-item>
  <el-menu-item index="widget">
    <span>组件</span>
  </el-menu-item>
  <el-menu-item index="theme">
    <span>主题</span>
  </el-menu-item>
  <el-menu-item index="setting">
    <span>设置</span>
  </el-menu-item>
</el-menu>
</template>


<style scoped>
.el-menu {
  height: 100%;
}

.el-menu--horizontal > .el-menu-item:nth-child(2) {
  margin-right: auto;
}
</style>
