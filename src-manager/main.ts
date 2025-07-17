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


/* ==== 项目全局变量 ==== */
import { spawnServer, axios } from './global'

// 启动服务器
const serverInfo = await spawnServer()

// Manager 设置 axios 参数
axios.defaults.baseURL = `http://${serverInfo.url}`
axios.defaults.headers.common['Authorization'] = `Bearer ${serverInfo.token}`

// Manager 向 Desktop 发送 axios 参数
const broadcast = new BroadcastChannel('axios')
broadcast.postMessage({url: serverInfo.url, token: serverInfo.token})


/* ==== 应用 ==== */
import { createApp } from 'vue'
import Manager from './Manager.vue'

const app = createApp(Manager)
  .use(router)
  .provide('$axios', axios)
  .mount('#manager')
