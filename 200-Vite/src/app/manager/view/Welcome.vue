<script lang="ts" setup>
/* ==== 欢迎视图 ==== */
import { ref } from 'vue'
import { ElCard, ElTag } from 'element-plus'

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

// const tips = ref([
//   '拖动部件到任意位置，打造专属布局',
//   '在设置中开启开机启动，让 Deskset 始终陪伴',
//   '使用 Material Symbols 图标库，统一视觉风格',
// ])

// const currentTip = ref(0)

// function nextTip() {
//   currentTip.value = (currentTip.value + 1) % tips.value.length
// }
</script>

<template>
  <div class="welcome-view">
    <!-- 顶部欢迎区 -->
    <section class="hero">
      <div class="hero-logo" />
      <h1 class="hero-title">欢迎使用数字桌搭</h1>
      <p class="hero-subtitle">一款桌面美化软件</p>
      <p class="hero-subtitle">基于 Tauri 框架开发</p>
      <p class="hero-subtitle">让桌面成为你的高效工作台</p>
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
    <!-- <section class="block">
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
    </section> -->
  </div>
</template>

<style scoped>
.welcome-view {
  padding: var(--view-padding);
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--view-gap);
}

/* ==== Hero ==== */
.hero {
  text-align: center;
  padding: 24px 24px 24px;
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
  gap: var(--view-card-grid-gap);
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

/* ==== Info Grid ==== */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--view-card-grid-gap-lg);
  width: 100%;
}

.info-card {
  min-width: 0;
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

@media (max-width: 700px) {
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .quick-grid,
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
