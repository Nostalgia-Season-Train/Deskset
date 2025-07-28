/* ==== CSS 文件 ==== */
import '../static/css/default-font.css'  // 默认字体

import '#shadcn/style.css'            // shadcn-vue 组件样式
import 'element-plus/dist/index.css'  // Element Plus 组件样式

import './style.css'


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


/* === 创建部件库、主题库 === */
import { exists, mkdir, BaseDirectory } from '@tauri-apps/plugin-fs'

const isWidgetLibExist = await exists('./widgets', { baseDir: BaseDirectory.Resource })
if (!isWidgetLibExist)
  await mkdir('./widgets', { baseDir: BaseDirectory.Resource })

const isThemeLibExist = await exists('./themes', { baseDir: BaseDirectory.Resource })
if (!isThemeLibExist)
  await mkdir('./themes', { baseDir: BaseDirectory.Resource })


/* ==== 项目全局变量 ==== */
import { spawnServer, axios } from './global'
import { error } from '@tauri-apps/plugin-log'

let isSpawn = true

try {
  // 启动服务器
  const serverInfo = await spawnServer()

  // Manager 设置 axios 参数
  axios.defaults.baseURL = `http://${serverInfo.url}`
  axios.defaults.headers.common['Authorization'] = `Bearer ${serverInfo.token}`

  // Manager 向 Desktop 发送 axios 参数
  const broadcast = new BroadcastChannel('axios')
  broadcast.postMessage({url: serverInfo.url, token: serverInfo.token})
} catch (err) {
  isSpawn = false
  error('Spawn DesksetBack Fail')
}

// 开发环境：无需考虑服务器是否启动成功
// @ts-ignore
const isDevEnv = import.meta.env.DEV as boolean

if (isDevEnv) {
  isSpawn = true
  axios.defaults.baseURL = 'http://127.0.0.1:6527'
}

// 初始化当前主题哈希表
import { activeThemeMap } from './global'
import { getThemes } from './main/theme'

const themes = await getThemes()
for (const theme of themes) {
  activeThemeMap.set(theme.name, theme)
}


/* ==== 应用 ==== */
import { createApp } from 'vue'
import Manager from './Manager.vue'

const app = createApp(Manager)
  .use(router)
  .provide('$axios', axios)
  .provide('$isSpawn', isSpawn)
  .mount('#manager')
