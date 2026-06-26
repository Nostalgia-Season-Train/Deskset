<script lang="ts" setup>
/* ==== 壁纸视图（参考 Wallpaper Engine） ==== */
import { ref } from 'vue'
import { ElButton, ElCard, ElInput, ElRadioButton, ElRadioGroup, ElTag } from 'element-plus'

type WallpaperType = 'image' | 'video' | 'web'

interface WallpaperItem {
  id: string
  name: string
  type: WallpaperType
  thumb: string
  author: string
  size: string
  active: boolean
}

const filterType = ref<WallpaperType | 'all'>('all')
const searchText = ref('')

const wallpapers = ref<WallpaperItem[]>([
  { id: 'wp-1', name: '宁静星空', type: 'image', thumb: '', author: 'Deskset', size: '4.2 MB', active: true },
  { id: 'wp-2', name: '雨天街道', type: 'video', thumb: '', author: 'Nostalgia', size: '32 MB', active: false },
  { id: 'wp-3', name: 'Pomodoro Timer', type: 'web', thumb: '', author: 'Community', size: '-', active: false },
  { id: 'wp-4', name: '日出山谷', type: 'image', thumb: '', author: 'Deskset', size: '6.8 MB', active: false },
])

const typeLabels: Record<WallpaperType, string> = {
  image: '图片',
  video: '视频',
  web: '网页',
}

const typeTags: Record<WallpaperType, 'primary' | 'success' | 'warning' | 'info'> = {
  image: 'primary',
  video: 'success',
  web: 'warning',
}

function applyWallpaper(id: string) {
  wallpapers.value.forEach((w) => (w.active = w.id === id))
}

function importWallpaper() {
  // 占位
}

function removeWallpaper(id: string) {
  wallpapers.value = wallpapers.value.filter((w) => w.id !== id)
}
</script>

<template>
  <div class="wallpaper-view">
    <!-- 工具栏 -->
    <el-card class="toolbar" shadow="hover">
      <div class="toolbar-inner">
        <el-input
          v-model="searchText"
          placeholder="搜索壁纸"
          clearable
          style="width: 220px"
        />
        <el-radio-group v-model="filterType">
          <el-radio-button value="all">全部</el-radio-button>
          <el-radio-button value="image">图片</el-radio-button>
          <el-radio-button value="video">视频</el-radio-button>
          <el-radio-button value="web">网页</el-radio-button>
        </el-radio-group>
        <el-button type="primary" @click="importWallpaper">导入壁纸</el-button>
      </div>
    </el-card>

    <!-- 壁纸网格 -->
    <div class="wallpaper-grid">
      <el-card
        v-for="wp in wallpapers"
        :key="wp.id"
        class="wallpaper-card"
        :class="{ active: wp.active }"
        shadow="hover"
      >
        <div class="thumb">
          <div class="thumb-placeholder">
            <span>{{ typeLabels[wp.type] }}</span>
          </div>
          <el-tag v-if="wp.active" type="success" class="active-tag">使用中</el-tag>
          <el-tag :type="typeTags[wp.type]" size="small" class="type-tag">
            {{ typeLabels[wp.type] }}
          </el-tag>
        </div>
        <div class="info">
          <div class="name">{{ wp.name }}</div>
          <div class="meta">{{ wp.author }} · {{ wp.size }}</div>
        </div>
        <div class="actions">
          <el-button size="small" type="primary" :disabled="wp.active" @click="applyWallpaper(wp.id)">
            应用
          </el-button>
          <el-button size="small" type="danger" plain @click="removeWallpaper(wp.id)">删除</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.wallpaper-view {
  padding: 16px;
}

.toolbar {
  margin-bottom: 16px;
}

.toolbar-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.wallpaper-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.wallpaper-card {
  transition: all 0.2s;
}

.wallpaper-card.active {
  border-color: var(--el-color-primary);
}

.thumb {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--el-fill-color-light);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  background: linear-gradient(135deg, var(--el-fill-color) 0%, var(--el-fill-color-light) 100%);
}

.active-tag {
  position: absolute;
  top: 8px;
  left: 8px;
}

.type-tag {
  position: absolute;
  top: 8px;
  right: 8px;
}

.info {
  margin-bottom: 8px;
}

.name {
  font-weight: 500;
  margin-bottom: 4px;
}

.meta {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.actions {
  display: flex;
  gap: 8px;
}
</style>
