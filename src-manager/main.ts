import { createApp } from 'vue'
import './style.css'

import 'element-plus/dist/index.css'  // Element Plus 组件样式，组件本身按需引入

import Manager from './Manager.vue'

import '../static/css/default-font.css'


/* ==== 动态路由 ==== */
import { createMemoryHistory, createRouter } from 'vue-router'

import Welcome from './routers/Welcome.vue'

const routes = [
  { path: '/', component: Welcome },

  { path: '/welcome', component: Welcome },
  { path: '/homepage', component: () => import('./routers/HomePage.vue') },
  { path: '/float',   component: () => import('./routers/Float.vue') },
  { path: '/widget',  component: () => import('./routers/Widget.vue') },
  { path: '/theme',   component: () => import('./routers/Theme.vue') },
  { path: '/setting', component: () => import('./routers/Setting.vue') }
]

const router = createRouter({
  history: createMemoryHistory(),
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


/* ==== 应用 ==== */
const app = createApp(Manager)
  .use(router)
  .provide('$axios', axios)
  .mount('#manager')
