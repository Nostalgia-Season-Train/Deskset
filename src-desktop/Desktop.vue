<script lang="ts" setup>
/* === 禁用默认事件 === */

// 刷新
document.addEventListener('keydown', (event: KeyboardEvent) => {
  if (
    event.key === 'F5' ||  // F5 刷新
    (event.ctrlKey && event.key === 'r') ||  // Windows/Linux 上：Ctrl + R 刷新
    (event.metaKey && event.key === 'r')     // Mac 上：Command + R 刷新
  ) {
    event.preventDefault()
  }
})

// 右键菜单
document.addEventListener('contextmenu', (event: MouseEvent) => {
  event.preventDefault()
})
</script>


<template>
<body>
  <RouterView />
</body>
</template>


<style lang="less" scoped>
* {
  margin: 0; padding: 0;
  user-select: none;
}
</style>
