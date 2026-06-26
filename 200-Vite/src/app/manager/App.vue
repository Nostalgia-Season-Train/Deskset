<script lang="ts" setup>
/* ==== 管理窗口主布局 ==== */
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const menus = [
  { path: '/welcome', label: '欢迎', icon: 'waving_hand' },
  { path: '/home', label: '主页', icon: 'home' },
  { path: '/widget', label: '部件', icon: 'extension' },
  { path: '/wallpaper', label: '壁纸', icon: 'image' },
  { path: '/theme', label: '主题', icon: 'palette' },
  { path: '/settings', label: '设置', icon: 'settings' },
]

const currentPath = computed(() => route.path)
const currentTitle = computed(() => {
  const m = menus.find((m) => m.path === route.path)
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
        <span class="material-symbols-outlined logo-icon">desktop_windows</span>
        <span class="logo-text">Deskset</span>
      </div>
      <nav class="nav">
        <button
          v-for="m in menus"
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
.app-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background: var(--el-fill-color-light);
  border-right: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-direction: column;
  padding: 16px 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 20px 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
  margin-bottom: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-weight: 600;
  font-size: 16px;
}

.nav {
  display: flex;
  flex-direction: column;
  padding: 0 8px;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 6px;
  color: var(--el-text-color-regular);
  font-size: 14px;
  text-align: left;
  transition: all 0.15s;
}

.nav-item:hover {
  background: var(--el-fill-color);
}

.nav-item.active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-weight: 500;
}

.nav-item.active .nav-icon {
  font-variation-settings:
    'FILL' 1,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

.nav-icon {
  font-size: 24px;
  width: 28px;
  text-align: center;
}

.main {
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

.topbar {
  height: 48px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--el-border-color-lighter);
  background: var(--el-bg-color);
}

.topbar-title {
  font-weight: 500;
}

.content {
  flex: 1;
  overflow: auto;
  background: var(--el-bg-color-page);
}

@media (max-width: 768px) {
  .app-layout {
    grid-template-columns: 64px 1fr;
  }

  .logo-text,
  .nav-label {
    display: none;
  }
}
</style>
