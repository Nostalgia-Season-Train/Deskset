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
import { readFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import axios from 'axios'

const getServerInfo = async () => {
  // 读取配置
  const data = await readFile(`./config/deskset.json`, { baseDir: BaseDirectory.Resource })
  const config = JSON.parse(new TextDecoder().decode(data))

  // 获取 port
  const port = config['server-port']

  // 获取 token
  const formData = new FormData()
  formData.append('username', config.username)
  formData.append('password', config.password)

  const repLogin = await axios.post(`http://127.0.0.1:${port}/v0/access/login`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  const token = repLogin.data.access_token

  // 返回 host、port 和 token
  return {
    host: '127.0.0.1',
    port: port,
    token: token
  }
}

const checkBackInterval = setInterval(async () => {
  try {
    const server = await getServerInfo()
    clearInterval(checkBackInterval)
    axios.defaults.baseURL = `http://${server.host}:${server.port}`
    axios.defaults.headers.common['Authorization'] = `Bearer ${server.token}`
    console.log('axios 初始化成功，后端上线！')
  } catch {}
}, 1000)


/* === 创建 Vue 应用 === */
import { createApp } from 'vue'
import './style.css'

import Desktop from './Desktop.vue'

import drag from './widgetDrag'  // 拖拽指令

const app = createApp(Desktop)
  .use(router)
  .use(drag)
  .provide('$axios', axios)
  .mount('#desktop')
