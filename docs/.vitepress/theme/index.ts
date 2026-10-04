import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import type { Theme } from 'vitepress'
import HomeFeatures from './HomeFeatures.vue'
import DownloadCard from './DownloadCard.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // 功能展示区：4 个功能纵向交替布局
      'home-features-before': () => h(HomeFeatures)
    })
  },
  enhanceApp({ app }: { app: import('vue').App }) {
    // 全局注册下载卡片组件
    app.component('DownloadCard', DownloadCard)
  }
} satisfies Theme
