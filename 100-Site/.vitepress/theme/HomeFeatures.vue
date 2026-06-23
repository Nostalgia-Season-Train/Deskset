<template>
  <div class="home-features">
    <div
      v-for="(feature, i) in features"
      :key="feature.title"
      class="feature-row"
      :class="{ reverse: i % 2 === 1 }"
    >
      <div class="feature-text">
        <div class="feature-icon">{{ feature.icon }}</div>
        <h2 class="feature-title">{{ feature.title }}</h2>
        <p class="feature-desc">{{ feature.desc }}</p>
        <p v-if="feature.badge" class="feature-badge">{{ feature.badge }}</p>
      </div>
      <div class="feature-image">
        <div class="image-placeholder">
          <span class="placeholder-text">示意图占位</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  {
    icon: '🖼️',
    title: '桌面美化',
    desc: '通过部件和动态壁纸装饰你的桌面。所有部件都能自由拖动、缩放、锁定和自动隐藏，把桌面布置成你想要的样子，再保存为主题一键分享。'
  },
  {
    icon: '📚️',
    title: 'Obsidian 联动',
    desc: '连接 Obsidian 笔记仓库，在桌面上直接管理日程与任务。创建数据库对笔记进行统计，以表格、画廊和看板等形式展示结果，让信息触手可及。'
  },
  {
    icon: '🔌',
    title: '插件系统',
    desc: '不止于内置部件。开发你自己的前端 Vue 部件和后端路由，打包成插件导入数字桌搭，扩展无限可能。'
  },
  {
    icon: '🤖',
    title: 'AI 桌宠',
    desc: '一只住在桌面上的智能 AI 宠物，陪你聊天、提醒日程、回答问题，让冷冰冰的桌面多一份温度。',
    badge: '开发中'
  }
]
</script>

<style scoped>
.home-features {
  max-width: 1152px;
  margin: 0 auto;
  padding: 64px 24px;
}

.feature-row {
  display: flex;
  align-items: center;
  gap: 48px;
  margin-bottom: 80px;
}

.feature-row:last-child {
  margin-bottom: 0;
}

.feature-row.reverse {
  flex-direction: row-reverse;
}

.feature-text {
  flex: 1;
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 16px;
  color: var(--vp-c-text-1);
}

.feature-desc {
  font-size: 16px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
  margin: 0;
}

.feature-badge {
  display: inline-block;
  margin-top: 16px;
  padding: 2px 12px;
  font-size: 13px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

.feature-image {
  flex: 1;
}

.image-placeholder {
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: 12px;
  background: var(--vp-c-bg-alt);
  border: 1px dashed var(--vp-c-border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  color: var(--vp-c-text-3);
  font-size: 16px;
}

@media (max-width: 768px) {
  .feature-row,
  .feature-row.reverse {
    flex-direction: column;
  }

  .feature-image {
    width: 100%;
  }
}
</style>
