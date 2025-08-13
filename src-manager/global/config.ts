import { reactive } from 'vue'

export const DEFAULT_SERVER_PORT = 6527
export const DEFAULT_USERNAME = 'username'
export const DEFAULT_PASSWORD = 'password'

// 持久化配置：数字桌搭存储在文件中的部分配置
export interface StorageConf {
  language: string
  closeBehavior: string
}

// 运行时配置：数字桌搭运行时所产生的完整配置，是 StorageConf 的超集
export interface RuntimeConf {
  language: string
  isAutostart: boolean
  closeBehavior: string

  server_port: number
  username: string
  password: string
}

export const config = reactive<RuntimeConf>({
  language: navigator.language.startsWith('zh') ? 'zh-cn' : 'en',
  isAutostart: false,
  closeBehavior: 'hide',

  server_port: DEFAULT_SERVER_PORT,
  username: DEFAULT_USERNAME,
  password: DEFAULT_PASSWORD
})
