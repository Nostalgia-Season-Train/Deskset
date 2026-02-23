<script lang="ts" setup>
/* === 组件 === */
import Aside from './ManagerAside.vue'
import Header from './ManagerHeader.vue'


/* === 路由 === */
import { useRouter } from 'vue-router'
const router = useRouter()
const jump = async (page: string) => {
  await router.push({ name: page })
}


/* === 服务器是否启动 === */
import { inject } from 'vue'
import Error from './routers/Error.vue'

const isSpawn = inject<boolean>('$isSpawn')


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

  <!-- 左导航栏 -->
  <aside>
    <Aside :router="router" @jump="jump"/>
  </aside>

  <main>
    <!-- 右标题栏 -->
    <header>
      <Header :router="router"/>
    </header>
    <!-- 右正文区：服务器正常 -->
    <article v-if="isSpawn">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component"/>
        </keep-alive>
      </router-view>
    </article>
    <!-- 右正文区：服务器不正常 -->
    <article v-if="!isSpawn">
      <Error/>
    </article>
  </main>

</body>
</template>


<style lang="less" scoped>
body {
  background: hsla(from var(--bg-dark) h s l / .65);
  display: flex;

  // calc 计算 aside、main 宽度，header、article 高度
    // 作用 1：固定布局宽度和高度
    // 作用 2：article>.content 设置 100% 宽高不会溢出窗口
  aside {
    z-index: 1;  // 跟 main 同一堆叠顺序，允许 main 中的元素覆盖
    width: var(--aside-width);
    height: 100vh;
  }
  main {
    z-index: 1;
    width: calc(100vw - var(--aside-width));
    height: 100vh;

    header {
      width: 100%;
      height: var(--header-height);
    }
    article {
      width: 100%;
      height: calc(100% - var(--header-height));
    }
  }
}
</style>
