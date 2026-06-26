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

// 资产统计
const assets = ref([
  { type: '字体', count: 12, size: '4.2 MB', icon: '🔤' },
  { type: '部件', count: 8, size: '2.1 MB', icon: '🧩' },
  { type: '壁纸', count: 24, size: '128 MB', icon: '🖼️' },
  { type: '主题', count: 3, size: '512 KB', icon: '🎨' },
])
</script>

<template>
  <div class="home-view">
    <!-- 桌面信息 -->
    <el-card class="card" shadow="hover">
      <template #header>
        <span>🖥️ 桌面信息</span>
      </template>
      <el-descriptions :column="2" border>
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
    </el-card>

    <!-- 资产管理 -->
    <el-card class="card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>📦 资产管理</span>
          <el-button type="primary" size="small" plain>刷新</el-button>
        </div>
      </template>
      <el-table :data="assets" stripe>
        <el-table-column label="类型" width="180">
          <template #default="{ row }">
            <span class="asset-icon">{{ row.icon }}</span>
            <span>{{ row.type }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="数量" width="120" align="center" />
        <el-table-column prop="size" label="占用空间" width="160" align="center" />
        <el-table-column label="操作" align="center">
          <template #default>
            <el-button size="small" link>查看</el-button>
            <el-button size="small" link type="primary">导入</el-button>
            <el-button size="small" link type="danger">清空</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.home-view {
  padding: 24px;
}

.card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.asset-icon {
  margin-right: 8px;
}
</style>
