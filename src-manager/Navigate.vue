<script setup>
const emit = defineEmits([
  "welcomePage",
  "supportPage",
  "widgetPage",
  "themePage",
  "developPage"
])

const handleSelect = (index) => {
  if (index == "welcome") {
    emit("welcomePage")
  } else if (index == "support") {
    emit("supportPage")
  } else if (index == "widget") {
    emit("widgetPage")
  } else if (index == "theme") {
    emit("themePage")
  } else if (index == "develop") {
    emit("developPage")
  }
}
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
  <el-menu-item index="widget">
    <span>组件</span>
  </el-menu-item>
  <el-menu-item index="theme">
    <span>主题</span>
  </el-menu-item>
  <el-menu-item index="develop">
    <span>开发</span>
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
