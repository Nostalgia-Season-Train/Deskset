<template>
  <div class="download-card">
    <!-- 加载中 -->
    <div v-if="loading" class="status">
      <span class="spinner" />
      <p>正在获取最新版本...</p>
    </div>

    <!-- 加载成功 -->
    <div v-else-if="release" class="release-info">
      <h2>Deskset v{{ release.version }}</h2>
      <p class="release-date">发布于 {{ release.date }}</p>

      <div class="download-actions">
        <a
          v-for="asset in release.assets"
          :key="asset.name"
          :href="asset.url"
          class="download-btn"
          :class="{ primary: asset.name.includes('.zip') }"
        >
          <span class="btn-icon">⬇</span>
          <span class="btn-text">{{ asset.label }}</span>
          <span class="btn-size">{{ asset.size }}</span>
        </a>
      </div>

      <a
        :href="`https://github.com/Nostalgia-Season-Train/Deskset/releases`"
        class="github-link"
        target="_blank"
        rel="noopener"
      >
        查看所有版本（GitHub 发布页）→
      </a>
    </div>

    <!-- 加载失败 -->
    <div v-else class="status error">
      <p>无法获取版本信息，请直接前往 GitHub 下载</p>
      <a
        href="https://github.com/Nostalgia-Season-Train/Deskset/releases"
        class="download-btn primary"
        target="_blank"
        rel="noopener"
      >
        前往 GitHub 发布页
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const GITHUB_API = 'https://api.github.com/repos/Nostalgia-Season-Train/Deskset/releases/latest'

const loading = ref(true)
const release = ref(null)

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

function assetLabel(name) {
  if (name.includes('win') || name.includes('.zip')) return 'Windows'
  if (name.includes('mac') || name.includes('.dmg')) return 'macOS'
  if (name.includes('linux') || name.includes('.AppImage')) return 'Linux'
  return name
}

onMounted(async () => {
  try {
    const res = await fetch(GITHUB_API)
    if (!res.ok) throw new Error('fetch failed')
    const data = await res.json()

    release.value = {
      version: data.tag_name.replace(/^v/, ''),
      date: new Date(data.published_at).toLocaleDateString('zh-CN'),
      assets: (data.assets || []).map(a => ({
        name: a.name,
        label: assetLabel(a.name),
        size: formatSize(a.size),
        url: a.browser_download_url
      }))
    }
  } catch (e) {
    release.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.download-card {
  max-width: 560px;
  margin: 24px 0;
  padding: 32px;
  border-radius: 12px;
  border: 1px solid var(--vp-c-border);
  background: var(--vp-c-bg-soft);
}

.status {
  text-align: center;
  padding: 24px 0;
  color: var(--vp-c-text-2);
}

.spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 3px solid var(--vp-c-border);
  border-top-color: var(--vp-c-brand-1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.release-info h2 {
  margin: 0 0 4px;
  font-size: 24px;
  color: var(--vp-c-text-1);
}

.release-date {
  margin: 0 0 24px;
  font-size: 14px;
  color: var(--vp-c-text-3);
}

.download-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-border);
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: border-color 0.25s, background 0.25s;
}

.download-btn:hover {
  border-color: var(--vp-c-brand-1);
}

.download-btn.primary {
  background: var(--vp-c-brand-1);
  color: #fff;
  border-color: var(--vp-c-brand-1);
}

.download-btn.primary:hover {
  background: var(--vp-c-brand-2);
}

.btn-icon {
  font-size: 18px;
}

.btn-text {
  flex: 1;
  font-weight: 600;
}

.btn-size {
  font-size: 13px;
  opacity: 0.7;
}

.github-link {
  display: inline-block;
  font-size: 14px;
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.github-link:hover {
  text-decoration: underline;
}

.error {
  color: var(--vp-c-text-2);
}
</style>
