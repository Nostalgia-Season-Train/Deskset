<script lang="ts" setup>
/* ==== 管理窗口主布局 ==== */
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const topMenus = [
  { path: '/welcome', label: '欢迎', icon: 'waving_hand' },
  { path: '/home', label: '主页', icon: 'home' },
]

const middleMenus = [
  { path: '/widget', label: '部件', icon: 'extension' },
  { path: '/wallpaper', label: '壁纸', icon: 'image' },
  { path: '/theme', label: '主题', icon: 'palette' },
]

const bottomMenus = [
  { path: '/settings', label: '设置', icon: 'settings' },
]

const allMenus = [...topMenus, ...middleMenus, ...bottomMenus]

const currentPath = computed(() => route.path)
const currentTitle = computed(() => {
  const m = allMenus.find((m) => m.path === route.path)
  return m ? m.label : ''
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
          <span class="material-symbols-outlined nav-icon">{{ m.icon }}</span>
          <span class="nav-label">{{ m.label }}</span>
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
          <span class="material-symbols-outlined nav-icon">{{ m.icon }}</span>
          <span class="nav-label">{{ m.label }}</span>
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
          <span class="material-symbols-outlined nav-icon">{{ m.icon }}</span>
          <span class="nav-label">{{ m.label }}</span>
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
