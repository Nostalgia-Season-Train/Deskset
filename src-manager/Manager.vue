<script setup>
/* 顶部导航 */
import Navigate from "./Navigate.vue"


/* 路由 */
import { useRouter } from "vue-router"

const router = useRouter()

const welcomePage = () => { router.push({ path: "/welcome" }) }
const supportPage = () => { router.push({ path: "/support" }) }
const widgetPage  = () => { router.push({ path: "/widget"  }) }
const themePage   = () => { router.push({ path: "/theme"   }) }
const settingPage = () => { router.push({ path: "/setting" }) }

/* 子程序，子窗口 */
import './child'
</script>


<template>
<body>
  <nav>
    <Navigate
      @welcomePage="welcomePage"
      @supportPage="supportPage"
      @widgetPage="widgetPage"
      @themePage="themePage"
      @settingPage="settingPage"
    />
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
