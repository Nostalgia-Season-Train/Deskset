/**
 * 管理窗口路由
 */
import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/welcome',
  },
  {
    path: '/welcome',
    name: 'welcome',
    component: () => import('../views/WelcomeView.vue'),
    meta: { title: '欢迎' },
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '主页' },
  },
  {
    path: '/widget',
    name: 'widget',
    component: () => import('../views/WidgetView.vue'),
    meta: { title: '部件' },
  },
  {
    path: '/wallpaper',
    name: 'wallpaper',
    component: () => import('../views/WallpaperView.vue'),
    meta: { title: '壁纸' },
  },
  {
    path: '/theme',
    name: 'theme',
    component: () => import('../views/ThemeView.vue'),
    meta: { title: '主题' },
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../views/SettingsView.vue'),
    meta: { title: '设置' },
  },
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
})
