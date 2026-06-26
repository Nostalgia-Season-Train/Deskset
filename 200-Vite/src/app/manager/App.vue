<script lang="ts" setup>
/* ==== 管理窗口主布局 ==== */
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 从路由表派生菜单，按 meta.group 分组
const menuRoutes = router.options.routes.filter((r) => r.meta?.group)
const topMenus = menuRoutes.filter((r) => r.meta!.group === 'top')
const middleMenus = menuRoutes.filter((r) => r.meta!.group === 'middle')
const bottomMenus = menuRoutes.filter((r) => r.meta!.group === 'bottom')

const currentPath = computed(() => route.path)
const currentTitle = computed(() => {
  const r = menuRoutes.find((r) => r.path === route.path)
  return r ? (r.meta!.title as string) : ''
})

function go(path: string) {
  router.push(path)
}
</script>

<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">
        <div class="logo-placeholder" />
        <span class="logo-text">Deskset</span>
      </div>
      <nav class="nav">
        <!-- 顶部菜单组 -->
        <button
          v-for="m in topMenus"
          :key="m.path"
          class="nav-item"
          :class="{ active: currentPath === m.path }"
          @click="go(m.path)"
        >
          <span class="material-symbols-outlined nav-icon">{{ m.meta!.icon }}</span>
          <span class="nav-label">{{ m.meta!.title }}</span>
        </button>

        <!-- 主页与部件之间的分割线 -->
        <div class="nav-divider" />

        <!-- 中部菜单组 -->
        <button
          v-for="m in middleMenus"
          :key="m.path"
          class="nav-item"
          :class="{ active: currentPath === m.path }"
          @click="go(m.path)"
        >
          <span class="material-symbols-outlined nav-icon">{{ m.meta!.icon }}</span>
          <span class="nav-label">{{ m.meta!.title }}</span>
        </button>

        <!-- 弹性占位，把设置推到底部 -->
        <div class="nav-spacer" />

        <!-- 底部菜单组 -->
        <button
          v-for="m in bottomMenus"
          :key="m.path"
          class="nav-item"
          :class="{ active: currentPath === m.path }"
          @click="go(m.path)"
        >
          <span class="material-symbols-outlined nav-icon">{{ m.meta!.icon }}</span>
          <span class="nav-label">{{ m.meta!.title }}</span>
        </button>
      </nav>
    </aside>

    <!-- 主区域 -->
    <main class="main">
      <header class="topbar">
        <span class="topbar-title">{{ currentTitle }}</span>
      </header>
      <div class="content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 样式已抽离至 style/app.less */
</style>
