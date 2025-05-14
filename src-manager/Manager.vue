<script lang="ts" setup>
/* === 组件 === */
import LeftNav from './Manager/LeftNav.vue'
import TopMenu from './Manager/TopMenu.vue'


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
    <TopMenu class="menu"/>
    <div class="content">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component"/>
        </keep-alive>
      </router-view>
    </div>
  </main>

</body>
</template>


<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
  user-select: none;
}
:deep(.el-scrollbar__thumb) {
  display: none;
}

body {
  --aside-width: 60px;  // 跟 LeftNav 组件 --fold-width 一致
  --menu-height: 35px;

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

    .menu {
      height: var(--menu-height);
      -webkit-app-region: drag;
    }
    .content {
      height: calc(100vh - var(--menu-height));
    }
  }
}
</style>
