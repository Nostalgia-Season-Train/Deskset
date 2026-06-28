<script lang="ts" setup>
/* ==== 主页视图：桌面信息 + 资产管理 ==== */
import { ref } from 'vue'
import { ElButton, ElCard, ElDescriptions, ElDescriptionsItem, ElTable, ElTableColumn } from 'element-plus'

// 桌面信息
const desktopInfo = ref({
  resolution: '1920 × 1080',
  dpi: 96,
  scaleFactor: 1.0,
  monitors: 1,
})

// 部件/壁纸/主题子卡片
const infoCards = ref([
  { label: '部件数量', value: 8, icon: 'extension' },
  { label: '当前壁纸', value: '宁静星空', icon: 'image' },
  { label: '当前主题', value: '默认主题', icon: 'palette' },
])

// 资产统计
const assets = ref([
  { type: '字体', count: 12, size: '4.2 MB', icon: 'text_fields' },
  { type: '部件', count: 8, size: '2.1 MB', icon: 'extension' },
  { type: '壁纸', count: 24, size: '128 MB', icon: 'image' },
  { type: '主题', count: 3, size: '512 KB', icon: 'palette' },
])
</script>

<template>
  <div class="home-view">
    <!-- 桌面信息 -->
    <el-card class="card" shadow="hover">
      <template #header>
        <span><span class="material-symbols-outlined">desktop_windows</span> 桌面信息</span>
      </template>
      <el-descriptions :column="2" border class="desktop-desc">
        <el-descriptions-item label="分辨率">
          {{ desktopInfo.resolution }}
        </el-descriptions-item>
        <el-descriptions-item label="DPI">
          {{ desktopInfo.dpi }}
        </el-descriptions-item>
        <el-descriptions-item label="缩放比例">
          {{ desktopInfo.scaleFactor * 100 }}%
        </el-descriptions-item>
        <el-descriptions-item label="显示器数量">
          {{ desktopInfo.monitors }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 部件/壁纸/主题子卡片 -->
      <div class="info-grid">
        <div v-for="(item, i) in infoCards" :key="i" class="info-item">
          <span class="material-symbols-outlined info-icon">{{ item.icon }}</span>
          <div class="info-text">
            <div class="info-label">{{ item.label }}</div>
            <div class="info-value">{{ item.value }}</div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 资产管理 -->
    <el-card class="card" shadow="hover">
      <template #header>
        <span><span class="material-symbols-outlined">inventory_2</span> 资产管理</span>
      </template>
      <el-table :data="assets" stripe>
        <el-table-column label="类型" width="180">
          <template #default="{ row }">
            <span class="material-symbols-outlined asset-icon">{{ row.icon }}</span>
            <span>{{ row.type }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="数量" width="120" align="center" />
        <el-table-column prop="size" label="占用空间" width="160" align="center" />
        <el-table-column label="操作" align="center">
          <template #default>
            <el-button size="small" link>查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.home-view {
  padding: var(--view-padding);
  display: flex;
  flex-direction: column;
  gap: var(--view-gap);
}

/* ==== 桌面信息 descriptions：标签列等宽 + 内容列均分 ==== */
.desktop-desc :deep(.el-descriptions__label) {
  width: 90px;
  min-width: 90px;
}

.desktop-desc :deep(.el-descriptions__table) {
  table-layout: fixed;
}

.desktop-desc :deep(.el-descriptions__cell) {
  width: 50%;
}

/* ==== 部件/壁纸/主题子卡片 ==== */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: var(--el-fill-color-light);
  border-radius: var(--el-border-radius-base);
}

.info-icon {
  font-size: 24px;
  color: var(--el-color-primary);
  flex-shrink: 0;
}

.info-text {
  min-width: 0;
}

.info-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 2px;
}

.info-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.asset-icon {
  margin-right: 8px;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
