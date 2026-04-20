import { reactive } from 'vue'

const generateRandomToken = (): string => {
  const array = new Uint8Array(32)
  crypto.getRandomValues(array)
  return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('')
}

export const DEFAULT_SERVER_PORT = 6527
export const DEFAULT_SERVER_TOKEN = generateRandomToken()

// 持久化配置：数字桌搭存储在文件中的部分配置
export interface StorageConf {
  language: string
  closeBehavior: string
  serverPort: number
  serverToken: string
}

// 运行时配置：数字桌搭运行时所产生的完整配置，是 StorageConf 的超集
export interface RuntimeConf {
  language: string
  isAutostart: boolean
  closeBehavior: string

  serverPort: number
  serverToken: string
  ai_base_url: string
  ai_api_key: string
  ai_model: string
}

export const config = reactive<RuntimeConf>({
  language: navigator.language.startsWith('zh') ? 'zh-cn' : 'en',
  isAutostart: false,
  closeBehavior: 'hide',

  serverPort: DEFAULT_SERVER_PORT,
  serverToken: DEFAULT_SERVER_TOKEN,
  ai_base_url: '',
  ai_api_key: '',
  ai_model: ''
})
