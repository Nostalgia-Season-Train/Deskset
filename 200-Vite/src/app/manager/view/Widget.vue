<script lang="ts" setup>
/* ==== 部件管理视图（参考 Rainmeter 风格） ==== */
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  ElButton,
  ElCard,
  ElDescriptions,
  ElDescriptionsItem,
  ElEmpty,
  ElForm,
  ElFormItem,
  ElInputNumber,
  ElSlider,
  ElSwitch,
} from 'element-plus'

interface WidgetItem {
  id: string
  name: string
  author: string
  version: string
  descript: string
  // 基础设置（CSS 属性）
  x: number
  y: number
  scale: number
  opacity: number
  // 状态切换（CSS 类名）
  dragLock: boolean
  disableInteract: boolean
  autoHide: boolean
}

// 部件列表
const widgets = ref<WidgetItem[]>([
  {
    id: 'datetime-clock',
    name: '数字时钟',
    author: 'Deskset',
    version: '1.0.0',
    descript: '简洁的数字时钟部件',
    x: 100, y: 50, scale: 1, opacity: 1,
    dragLock: false, disableInteract: false, autoHide: false,
  },
  {
    id: 'weather-today',
    name: '今日天气',
    author: 'Nostalgia',
    version: '2.1.0',
    descript: '展示当前天气和未来 3 小时预报',
    x: 300, y: 200, scale: 1.2, opacity: 0.9,
    dragLock: true, disableInteract: false, autoHide: true,
  },
])

const currentId = ref<string | null>(widgets.value[0]?.id ?? null)
const current = computed(() => widgets.value.find((w) => w.id === currentId.value))

function addWidget() {
  const id = `widget-${Date.now()}`
  widgets.value.push({
    id,
    name: '新部件',
    author: 'Unknown',
    version: '0.1.0',
    descript: '尚未描述',
    x: 0, y: 0, scale: 1, opacity: 1,
    dragLock: false, disableInteract: false, autoHide: false,
  })
  currentId.value = id
  ElMessage.success('已添加部件')
}

function clearWidgets() {
  widgets.value = []
  currentId.value = null
  ElMessage.warning('已清空部件列表')
}

function selectWidget(id: string) {
  currentId.value = id
}

function deleteWidget(id: string) {
  const idx = widgets.value.findIndex((w) => w.id === id)
  if (idx >= 0) {
    widgets.value.splice(idx, 1)
    if (currentId.value === id) {
      currentId.value = widgets.value[0]?.id ?? null
    }
    ElMessage.success('已删除部件')
  }
}

function editWidget() {
  ElMessage.info('编辑部件内部模型（暂未实现）')
}

function locateWidget() {
  ElMessage.info('通过红框标识部件在桌面的位置（暂未实现）')
}
</script>

<template>
  <div class="widget-view">
    <!-- 左侧：部件列表 -->
    <el-card class="panel panel-list" shadow="hover">
      <template #header>
        <div class="panel-header">
          <span><span class="material-symbols-outlined">extension</span> 部件列表</span>
          <div>
            <el-button size="small" type="primary" @click="addWidget">添加部件</el-button>
            <el-button size="small" type="danger" plain @click="clearWidgets">清空</el-button>
          </div>
        </div>
      </template>
      <div class="widget-list">
        <el-button
          v-for="w in widgets"
          :key="w.id"
          class="widget-item"
          :type="w.id === currentId ? 'primary' : 'default'"
          @click="selectWidget(w.id)"
        >
          <span class="widget-name">{{ w.name }}</span>
          <span class="widget-ver">v{{ w.version }}</span>
        </el-button>
        <el-empty v-if="widgets.length === 0" description="暂无部件" :image-size="80" />
      </div>
    </el-card>

    <!-- 右侧：部件详情 -->
    <div class="panel-detail">
      <template v-if="current">
        <!-- 部件信息 -->
        <el-card class="panel" shadow="hover">
          <template #header>
            <span><span class="material-symbols-outlined">info</span> 部件信息</span>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="名称">{{ current.name }}</el-descriptions-item>
            <el-descriptions-item label="作者">{{ current.author }}</el-descriptions-item>
            <el-descriptions-item label="版本">{{ current.version }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ current.descript }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 部件操作 -->
        <el-card class="panel" shadow="hover">
          <template #header>
            <span><span class="material-symbols-outlined">build</span> 部件操作</span>
          </template>
          <div class="ops">
            <el-button type="danger" @click="deleteWidget(current.id)">删除</el-button>
            <el-button type="primary" @click="editWidget">编辑</el-button>
            <el-button @click="locateWidget">定位</el-button>
          </div>
        </el-card>

        <!-- 部件基础设置（CSS 属性） -->
        <el-card class="panel" shadow="hover">
          <template #header>
            <span><span class="material-symbols-outlined">tune</span> 基础设置（CSS 属性）</span>
          </template>
          <el-form label-width="80px">
            <el-form-item label="坐标">
              <el-input-number v-model="current.x" :step="1" />
            </el-form-item>
            <el-form-item label="坐标">
              <el-input-number v-model="current.y" :step="1" />
            </el-form-item>
            <el-form-item label="缩放">
              <el-slider v-model="current.scale" :min="0" :max="4" :step="0.1" />
            </el-form-item>
            <el-form-item label="透明度">
              <el-slider v-model="current.opacity" :min="0" :max="1" :step="0.01" />
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 部件状态切换（CSS 类名） -->
        <el-card class="panel" shadow="hover">
          <template #header>
            <span><span class="material-symbols-outlined">sync</span> 状态切换（CSS 类名）</span>
          </template>
          <el-form label-width="160px">
            <el-form-item label="锁定拖动">
              <el-switch v-model="current.dragLock" />
            </el-form-item>
            <el-form-item label="禁用交互">
              <el-switch v-model="current.disableInteract" />
            </el-form-item>
            <el-form-item label="自动隐藏">
              <el-switch v-model="current.autoHide" />
            </el-form-item>
          </el-form>
        </el-card>
      </template>

      <el-empty v-else description="请从左侧选择一个部件" />
    </div>
  </div>
</template>

<style scoped>
.widget-view {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 16px;
  padding: 16px;
  height: 100%;
  overflow: auto;
}

.panel {
  margin-bottom: 16px;
}

.panel-list {
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
}

.panel-list :deep(.el-card__body) {
  flex: 1;
  overflow: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.widget-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.widget-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 44px;
}

.widget-name {
  font-weight: 500;
}

.widget-ver {
  font-size: 12px;
  opacity: 0.7;
}

.panel-detail {
  min-width: 0;
}

.ops {
  display: flex;
  gap: 12px;
}

@media (max-width: 700px) {
  .widget-view {
    grid-template-columns: 1fr;
  }
}
</style>
