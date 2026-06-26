<script lang="ts" setup>
/* ==== 欢迎视图 ==== */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElCard, ElTag } from 'element-plus'

const router = useRouter()

const version = ref('0.1.0')
const releaseDate = ref('2024-12')

const stats = ref([
  { label: '部件', value: 8, icon: 'extension' },
  { label: '壁纸', value: 24, icon: 'image' },
  { label: '主题', value: 3, icon: 'palette' },
  { label: '插件', value: 5, icon: 'puzzle' },
])

const quickActions = ref([
  { title: '添加部件', desc: '从本地或市场导入新部件', icon: 'add_circle', path: '/widget' },
  { title: '更换壁纸', desc: '浏览并应用壁纸资源', icon: 'image', path: '/wallpaper' },
  { title: '切换主题', desc: '应用已有主题或自定义', icon: 'palette', path: '/theme' },
  { title: '查看设置', desc: '调整软件偏好', icon: 'settings', path: '/settings' },
])

const changelog = ref([
  { date: '2024-12', tag: '新增', text: '桌面部件管理系统' },
  { date: '2024-12', tag: '新增', text: 'Obsidian 仓库联动' },
  { date: '2024-11', tag: '修复', text: '修复窗口拖动延迟问题' },
  { date: '2024-11', tag: '优化', text: '主题切换性能优化' },
])

const news = ref([
  { title: '插件市场上线', date: '2024-12-01', desc: '现已支持第三方插件导入' },
  { title: 'AI 桌宠内测开启', date: '2024-11-20', desc: '邀请用户体验 AI 桌宠功能' },
])

const tips = ref([
  '拖动部件到任意位置，打造专属布局',
  '在设置中开启开机启动，让 Deskset 始终陪伴',
  '使用 Material Symbols 图标库，统一视觉风格',
])

const currentTip = ref(0)

function goHome() {
  router.push('/home')
}

function go(path: string) {
  router.push(path)
}

function nextTip() {
  currentTip.value = (currentTip.value + 1) % tips.value.length
}
</script>

<template>
  <div class="welcome-view">
    <!-- 顶部欢迎区 -->
    <section class="hero">
      <div class="hero-logo" />
      <h1 class="hero-title">欢迎使用数字桌搭 Deskset</h1>
      <p class="hero-subtitle">一款桌面美化软件 · 基于 Tauri 框架开发</p>
      <p class="hero-slogan">让桌面成为专属于你的高效工作台</p>
      <div class="hero-version">v{{ version }} · {{ releaseDate }}</div>
      <div class="hero-actions">
        <el-button type="primary" size="large" @click="goHome">进入主页</el-button>
        <el-button size="large" @click="go('/widget')">快速开始</el-button>
      </div>
    </section>

    <!-- 统计数据 -->
    <section class="stats">
      <el-card v-for="(s, i) in stats" :key="i" class="stat-card">
        <div class="stat">
          <span class="material-symbols-outlined stat-icon">{{ s.icon }}</span>
          <div class="stat-info">
            <div class="stat-value">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </el-card>
    </section>

    <!-- 快速操作 -->
    <section class="block">
      <div class="block-header">
        <h2 class="block-title">快速操作</h2>
      </div>
      <div class="quick-grid">
        <el-card
          v-for="(a, i) in quickActions"
          :key="i"
          class="quick-card"
          @click="go(a.path)"
        >
          <div class="quick">
            <span class="material-symbols-outlined quick-icon">{{ a.icon }}</span>
            <div class="quick-text">
              <div class="quick-title">{{ a.title }}</div>
              <div class="quick-desc">{{ a.desc }}</div>
            </div>
            <span class="material-symbols-outlined quick-arrow">chevron_right</span>
          </div>
        </el-card>
      </div>
    </section>

    <!-- 双栏：更新日志 + 社区新闻 -->
    <section class="info-grid">
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title"><span class="material-symbols-outlined">description</span> 更新日志</span>
            <el-tag size="small" type="info">Changelog</el-tag>
          </div>
        </template>
        <ul class="list">
          <li v-for="(item, i) in changelog" :key="i" class="changelog-item">
            <span class="changelog-date">{{ item.date }}</span>
            <el-tag
              :type="item.tag === '新增' ? 'success' : item.tag === '修复' ? 'warning' : 'info'"
              size="small"
            >
              {{ item.tag }}
            </el-tag>
            <span class="changelog-text">{{ item.text }}</span>
          </li>
        </ul>
      </el-card>

      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span class="card-title"><span class="material-symbols-outlined">newspaper</span> 社区新闻</span>
            <el-tag size="small" type="info">News</el-tag>
          </div>
        </template>
        <ul class="list">
          <li v-for="(item, i) in news" :key="i" class="news-item">
            <div class="news-title">{{ item.title }}</div>
            <div class="news-desc">{{ item.desc }}</div>
            <div class="news-date">{{ item.date }}</div>
          </li>
        </ul>
      </el-card>
    </section>

    <!-- 小贴士 -->
    <section class="block">
      <el-card class="tip-card" @click="nextTip">
        <div class="tip">
          <span class="material-symbols-outlined tip-icon">lightbulb</span>
          <div class="tip-content">
            <div class="tip-label">小贴士</div>
            <div class="tip-text">{{ tips[currentTip] }}</div>
          </div>
          <span class="material-symbols-outlined tip-next">swap_horiz</span>
        </div>
      </el-card>
    </section>
  </div>
</template>

<style scoped>
.welcome-view {
  padding: 32px 24px;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ==== Hero ==== */
.hero {
  text-align: center;
  padding: 40px 24px 24px;
}

.hero-logo {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: var(--el-color-primary);
  margin: 0 auto 20px;
}

.hero-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px;
}

.hero-subtitle {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0 0 4px;
}

.hero-slogan {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0 0 20px;
}

.hero-version {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  margin-bottom: 20px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* ==== Stats ==== */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.stat-card {
  cursor: default;
}

.stat {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 24px;
  color: var(--el-color-primary);
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

/* ==== Block ==== */
.block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.block-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.block-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0;
}

/* ==== Quick Actions ==== */
.quick-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.quick-card {
  cursor: pointer;
  transition: border-color 0.15s;
}

.quick-card:hover {
  border-color: var(--el-color-primary) !important;
}

.quick {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quick-icon {
  font-size: 24px;
  color: var(--el-color-primary);
}

.quick-text {
  flex: 1;
  min-width: 0;
}

.quick-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.quick-desc {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.quick-arrow {
  font-size: 20px;
  color: var(--el-text-color-placeholder);
}

/* ==== Info Grid ==== */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.changelog-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.changelog-item:last-child {
  border-bottom: none;
}

.changelog-date {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  min-width: 56px;
}

.changelog-text {
  flex: 1;
  font-size: 13px;
}

.news-item {
  padding: 10px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.news-item:last-child {
  border-bottom: none;
}

.news-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.news-desc {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  margin-bottom: 4px;
}

.news-date {
  color: var(--el-text-color-placeholder);
  font-size: 12px;
}

/* ==== Tip ==== */
.tip-card {
  cursor: pointer;
  transition: border-color 0.15s;
}

.tip-card:hover {
  border-color: var(--el-color-primary) !important;
}

.tip {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tip-icon {
  font-size: 24px;
  color: var(--el-color-warning);
}

.tip-content {
  flex: 1;
}

.tip-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 2px;
}

.tip-text {
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.tip-next {
  font-size: 20px;
  color: var(--el-text-color-placeholder);
}

@media (max-width: 768px) {
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .quick-grid,
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
