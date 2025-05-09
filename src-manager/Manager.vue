<script lang="ts" setup>
/* === 组件 === */
import LeftNav from './Manager/LeftNav.vue'


/* === 路由 === */
import { useRouter } from 'vue-router'
const router = useRouter()
const jump = async (page: string) => {
  router.push({ path: `/${page}` })
}
</script>


<template>
<body>

  <aside>
    <LeftNav @jump="jump"/>
  </aside>

  <main>
    <RouterView />
  </main>

</body>
</template>


<style lang="less" scoped>
* {
  margin: 0; padding: 0;
  user-select: none;
}

body {
  --aside-width: 60px;  // 跟 LeftNav 组件 --fold-width 一致

  background-color: #3331;
  display: flex;

  aside {
    z-index: 2;
    width: var(--aside-width);
    height: 100vh;
    -webkit-app-region: drag;
  }
  main {
    z-index: 1;
    width: calc(100vw - var(--aside-width));
    height: 100vh;
    -webkit-app-region: drag;
  }
}
</style>
