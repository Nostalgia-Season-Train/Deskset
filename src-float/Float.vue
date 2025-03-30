<template>
<body>
  <Suspense><!-- 能让 setup 顶层使用 await -->
    <RouterView />
  </Suspense>
</body>
</template>


<style lang="less" scoped>
* {
  margin: 0; padding: 0;
  user-select: none;
}
</style>
