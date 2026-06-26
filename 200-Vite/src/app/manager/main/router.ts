/**
 * 管理窗口路由
 *
 * meta 字段：
 * - title: 显示名称
 * - icon: Material Symbols 图标名（https://fonts.google.com/icons）
 * - group: 导航分组（top/middle/bottom）
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
    meta: { title: '欢迎', icon: 'waving_hand', group: 'top' },
  }, {
    path: '/home',
    name: 'home',
    component: () => import('../view/Home.vue'),
    meta: { title: '主页', icon: 'home', group: 'top' },
  }, {
    path: '/widget',
    name: 'widget',
    component: () => import('../view/Widget.vue'),
    meta: { title: '部件', icon: 'extension', group: 'middle' },
  }, {
    path: '/wallpaper',
    name: 'wallpaper',
    component: () => import('../view/Wallpaper.vue'),
    meta: { title: '壁纸', icon: 'image', group: 'middle' },
  }, {
    path: '/theme',
    name: 'theme',
    component: () => import('../view/Theme.vue'),
    meta: { title: '主题', icon: 'palette', group: 'middle' },
  }, {
    path: '/settings',
    name: 'settings',
    component: () => import('../view/Setting.vue'),
    meta: { title: '设置', icon: 'settings', group: 'bottom' },
  },
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
})
