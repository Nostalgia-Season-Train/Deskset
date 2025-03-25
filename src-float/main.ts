/* === 默认字体 === */
import '../static/css/default-font.css'


/* === 动态路由 === */

// 遍历 pages 注册 routes
const routes: any = []

const pages = import.meta.glob('./subfloats/*.vue')
for (const page in pages) {
  // 注：
    // 路径必须以 / 开头
    // 中文路径通过百分号编码访问
    // page：./pages/page.vue 和 pages[page]：() => import("/src-float/pages/page.vue")
  const name = page.replace('.vue', '').split('/').pop()
  const encodeName = encodeURIComponent(String(name))
  routes.push({ path: `/${encodeName}`, component: pages[page] })
}

// 创建 Router
import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),  // Hash 模式：float.html#/page 访问
  routes: routes
})


/* === 创建 Vue 应用 === */
import { createApp } from 'vue'
import './style.css'

import Float from './Float.vue'

const app = createApp(Float)
  .use(router)
  .mount('#float')
