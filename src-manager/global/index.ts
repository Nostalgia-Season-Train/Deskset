/* ==== 项目全局变量 ==== */
  // 由各 Vue 组件使用，通过 ES6 模块机制实现单例模式
  // 通过 main.ts 初始化

export * from './widget'
export * from './theme'

export * from './child/server'
export * from './win/manager'
export * from './page/desktop'

export { default as axios } from 'axios'
