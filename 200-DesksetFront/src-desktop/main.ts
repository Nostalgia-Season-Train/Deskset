/* === 静态样式 === */
import 'element-plus/dist/index.css'     // Element Plus 默认样式
import '../static/css/default-font.css'  // 默认字体


/* === 动态路由 === */
  // 代码注释参见：src-float/main.ts
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('./DesktopMain.vue') },
  { path: '/Main', component: () => import('./DesktopMain.vue') }
]

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


/* ==== axios ==== */
import axios from 'axios'
import { AxiosChannel } from './global/channel'

const initAxios = async () => {
  const broadcast = AxiosChannel

  return new Promise((resolve, reject) => {
    broadcast.onmessage = (ev) => {
      const serverInfo = ev.data
      axios.defaults.baseURL = `http://${serverInfo.url}`
      axios.defaults.headers.common['Authorization'] = `Bearer ${serverInfo.token}`
      resolve()
    }
  })
}

// 开发环境：不等待 Axios 消息，方便刷新
const isDevEnv = import.meta.env.DEV

if (isDevEnv) {
  axios.defaults.baseURL = 'http://127.0.0.1:6527'
} else {
  await initAxios()
}


/* === 上下文 === */
  // 通过 const XXX = $deskset_vue 导入 Vue 依赖
import * as Vue from 'vue'
import Axios from 'axios'
import * as Element_Plus from 'element-plus'
import * as Vue_Hooks_Plus from 'vue-hooks-plus'

window.$deskset_vue = Vue
window.$deskset_axios = Axios
window.$deskset_element_plus = Element_Plus
window.$deskset_vue_hooks_plus = Vue_Hooks_Plus


/* === 创建 Vue 应用 === */
import { createApp } from 'vue'
import './style.css'

import Desktop from './Desktop.vue'

const app = createApp(Desktop)
  .use(router)
  .provide('$axios', axios)
  .mount('#desktop')
