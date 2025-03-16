import { createApp } from 'vue'
import './style.css'

import 'element-plus/dist/index.css'  // Element Plus 组件样式，组件本身按需引入

import Manager from './Manager.vue'

import '../static/css/default-font.css'


// 动态路由
import { createMemoryHistory, createRouter } from 'vue-router'

import Welcome from './routers/Welcome.vue'

const routes = [
  { path: '/', component: Welcome },

  { path: '/welcome', component: Welcome },
  { path: '/support', component: () => import('./routers/Support.vue') },
  { path: '/float',   component: () => import('./routers/Float.vue') },
  { path: '/widget',  component: () => import('./routers/Widget.vue') },
  { path: '/theme',   component: () => import('./routers/Theme.vue') },
  { path: '/setting', component: () => import('./routers/Setting.vue') }
]

const router = createRouter({
  history: createMemoryHistory(),
  routes: routes
})


// 持久化
import { createPinia } from 'pinia'

const pinia = createPinia()


// 应用
const app = createApp(Manager)
  .use(router)
  .use(pinia)
  .mount('#manager')
