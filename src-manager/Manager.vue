<script lang="ts" setup>
/* 顶部导航 */
import Navigate from "./Navigate.vue"


/* 路由 */
import { useRouter } from "vue-router"

const router = useRouter()

const jumpPage = async (page: string) => { router.push({ path: `/${page}` }) }


/* 子程序，子窗口 */
import './child'
</script>


<template>
<body>
  <nav>
    <Navigate @jumpPage="jumpPage"/>
  </nav>
  <main>
    <RouterView />
  </main>
</body>
</template>


<style scoped>
* {
  margin: 0; padding: 0;
  user-select: none;
}

nav {
  height: 10vh;
}
main {
  height: 90vh;
}
</style>
