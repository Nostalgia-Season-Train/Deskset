/* === 静态样式 === */
import 'element-plus/dist/index.css'     // Element Plus 默认样式
import '../static/css/default-font.css'  // 默认字体


/* === 动态路由 === */
  // 代码注释参见：src-float/main.ts
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [{ path: '/', component: () => import('./DesktopMain.vue') }]

const pages = import.meta.glob('./subdesktops/*.vue')
for (const page in pages) {
  const name = page.replace('.vue', '').split('/').pop()
  const encodeName = encodeURIComponent(String(name))
  routes.push({ path: `/${encodeName}`, component: pages[page] })
}

const router = createRouter({
  history: createWebHashHistory(),
  routes: routes
})


/* === 创建 Vue 应用 === */
import { createApp } from 'vue'
import './style.css'

import Desktop from './Desktop.vue'

import drag from './widgetDrag'  // 拖拽指令

const app = createApp(Desktop)
  .use(router)
  .use(drag)
  .mount('#desktop')
