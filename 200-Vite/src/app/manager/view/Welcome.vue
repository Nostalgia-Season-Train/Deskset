<script lang="ts" setup>
/* ==== 欢迎视图 ==== */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElCard, ElTag } from 'element-plus'

const router = useRouter()

const version = ref('0.1.0')
const releaseDate = ref('2024-12')

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

function goHome() {
  router.push('/home')
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
      <el-button type="primary" size="large" @click="goHome">进入主页</el-button>
    </section>

    <!-- 中部双栏：更新日志 + 社区新闻 -->
    <section class="info-grid">
      <!-- 更新日志 -->
      <el-card class="info-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><span class="material-symbols-outlined">description</span> 更新日志</span>
            <el-tag size="small" type="info">Changelog</el-tag>
          </div>
        </template>
        <ul class="changelog-list">
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

      <!-- 社区新闻 -->
      <el-card class="info-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><span class="material-symbols-outlined">newspaper</span> 社区新闻</span>
            <el-tag size="small" type="info">News</el-tag>
          </div>
        </template>
        <ul class="news-list">
          <li v-for="(item, i) in news" :key="i" class="news-item">
            <div class="news-title">{{ item.title }}</div>
            <div class="news-desc">{{ item.desc }}</div>
            <div class="news-date">{{ item.date }}</div>
          </li>
        </ul>
      </el-card>
    </section>
  </div>
</template>

<style scoped>
.welcome-view {
  padding: 32px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 48px 24px 32px;
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

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 32px;
}

.info-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.changelog-list,
.news-list {
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
  font-size: 13px;
  min-width: 64px;
}

.changelog-text {
  flex: 1;
}

.news-item {
  padding: 12px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.news-item:last-child {
  border-bottom: none;
}

.news-title {
  font-weight: 500;
  margin-bottom: 4px;
}

.news-desc {
  color: var(--el-text-color-regular);
  font-size: 13px;
  margin-bottom: 4px;
}

.news-date {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
