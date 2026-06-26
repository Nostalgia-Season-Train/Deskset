/**
 * 管理窗口路由
 */
import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/welcome',
  }, {
    path: '/welcome',
    name: 'welcome',
    component: () => import('../view/Welcome.vue'),
    meta: { title: '欢迎' },
  }, {
    path: '/home',
    name: 'home',
    component: () => import('../view/Home.vue'),
    meta: { title: '主页' },
  }, {
    path: '/widget',
    name: 'widget',
    component: () => import('../view/Widget.vue'),
    meta: { title: '部件' },
  }, {
    path: '/wallpaper',
    name: 'wallpaper',
    component: () => import('../view/Wallpaper.vue'),
    meta: { title: '壁纸' },
  }, {
    path: '/theme',
    name: 'theme',
    component: () => import('../view/Theme.vue'),
    meta: { title: '主题' },
  }, {
    path: '/settings',
    name: 'settings',
    component: () => import('../view/Setting.vue'),
    meta: { title: '设置' },
  },
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
})
