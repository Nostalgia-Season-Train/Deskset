<script lang="ts" setup>
/* ==== 主题视图：导出主题包（非内联字体、部件、壁纸） ==== */
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ElButton, ElCard, ElInput, ElTable, ElTableColumn } from 'element-plus'

interface ThemeItem {
  id: string
  name: string
  preview: string
  savedAt: string
  note: string
  active: boolean
}

const searchText = ref('')

const themes = ref<ThemeItem[]>([
  {
    id: 't-1',
    name: '默认主题',
    preview: '',
    savedAt: '2024-12-01 10:30',
    note: '简洁明亮的默认配色',
    active: true,
  },
  {
    id: 't-2',
    name: '暗夜模式',
    preview: '',
    savedAt: '2024-11-28 18:12',
    note: '护眼暗色主题',
    active: false,
  },
  {
    id: 't-3',
    name: '赛博朋克',
    preview: '',
    savedAt: '2024-11-20 09:45',
    note: '霓虹光效 + 紫黑配色',
    active: false,
  },
])

function applyTheme(id: string) {
  themes.value.forEach((t) => (t.active = t.id === id))
  ElMessage.success('主题已应用')
}

function deleteTheme(id: string) {
  themes.value = themes.value.filter((t) => t.id !== id)
}

function saveTheme() {
  ElMessage.success('当前配置已保存为主题')
}

function importTheme() {
  ElMessage.info('导入主题包（暂未实现）')
}

function exportTheme() {
  ElMessage.info('导出主题包（非内联字体、部件、壁纸）')
}
</script>

<template>
  <div class="theme-view">
    <!-- 工具栏 -->
    <el-card class="toolbar" shadow="hover">
      <div class="toolbar-inner">
        <el-input
          v-model="searchText"
          placeholder="搜索主题"
          clearable
          style="width: 220px"
        />
        <div class="spacer" />
        <el-button type="primary" @click="saveTheme">保存</el-button>
        <el-button @click="importTheme">导入</el-button>
        <el-button @click="exportTheme">导出</el-button>
      </div>
    </el-card>

    <!-- 主题表格 -->
    <el-card shadow="hover">
      <el-table :data="themes" stripe>
        <el-table-column label="预览图" width="120" align="center">
          <template #default="{ row }">
            <div class="preview">
              <div class="preview-placeholder">{{ row.name.charAt(0) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="主题名称" width="180" />
        <el-table-column prop="savedAt" label="保存时间" width="180" align="center" />
        <el-table-column prop="note" label="主题注释" min-width="200" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="{ row }">
            <el-button
              size="small"
              type="primary"
              :disabled="row.active"
              @click="applyTheme(row.id)"
            >
              应用
            </el-button>
            <el-button
              size="small"
              type="danger"
              plain
              :disabled="row.active"
              @click="deleteTheme(row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.theme-view {
  padding: 16px;
}

.toolbar {
  margin-bottom: 16px;
}

.toolbar-inner {
  display: flex;
  align-items: center;
  gap: 12px;
}

.spacer {
  flex: 1;
}

.preview {
  width: 80px;
  height: 48px;
  margin: 0 auto;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--el-color-primary-light-7), var(--el-color-primary-light-5));
  color: var(--el-color-primary);
  font-weight: 600;
  border-radius: 4px;
}
</style>
