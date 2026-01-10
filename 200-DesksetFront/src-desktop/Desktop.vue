<script lang="ts" setup>
/* === 生产环境：禁用默认事件 === */
if (!import.meta.env.DEV as boolean) {
  // 刷新和开发者工具
  document.addEventListener('keydown', (event: KeyboardEvent) => {
    if (
      event.key === 'F5' ||  // F5 刷新
      (event.ctrlKey && event.key === 'r') ||  // Windows/Linux 上：Ctrl + R 刷新
      (event.metaKey && event.key === 'r') ||  // Mac 上：Command + R 刷新
      event.key === 'F12' ||  // F12 开发者工具
      (event.ctrlKey && event.key === 'f')  // Ctrl + F 搜索
    ) {
      event.preventDefault()
    }
  })
  // 右键菜单
  document.addEventListener('contextmenu', (event: MouseEvent) => {
    event.preventDefault()
  })
}
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
