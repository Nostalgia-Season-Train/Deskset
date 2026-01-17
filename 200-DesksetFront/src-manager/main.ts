/* ==== CSS 文件 ==== */
import '../static/css/default-font.css'  // 默认字体

import '#shadcn/style.css'            // shadcn-vue 组件样式
import 'element-plus/dist/index.css'  // Element Plus 组件样式

import './style.css'


/* ==== 动态路由 ==== */
import { createMemoryHistory, createRouter } from 'vue-router'

const routes = [
  { path: '/welcome', name: 'welcome', component: () => import('./routers/Welcome.vue') },
  { path: '/widget',  name: 'widget',  component: () => import('./routers/Widget.vue') },
  { path: '/theme',   name: 'theme',   component: () => import('./routers/Theme.vue') },
  { path: '/setting', name: 'setting', component: () => import('./routers/Setting.vue') }
]

const router = createRouter({
  history: createMemoryHistory(),
  routes: routes
})

await router.push({ name: 'welcome' })  // 确保 router.currentRoute.value.name 拿到有效值


/* ==== 创建配置目录、部件库、主题库 ==== */
import { exists, mkdir, BaseDirectory } from '@tauri-apps/plugin-fs'

const isConfigDirExist = await exists('./config', { baseDir: BaseDirectory.Resource })
if (!isConfigDirExist)
  await mkdir('./config', { baseDir: BaseDirectory.Resource })

const isWidgetLibExist = await exists('./widgets', { baseDir: BaseDirectory.Resource })
if (!isWidgetLibExist)
  await mkdir('./widgets', { baseDir: BaseDirectory.Resource })

const isThemeLibExist = await exists('./themes', { baseDir: BaseDirectory.Resource })
if (!isThemeLibExist)
  await mkdir('./themes', { baseDir: BaseDirectory.Resource })



/* =========================== */
/* =                         = */
/* =    软件生命: 状态构造    = */
/* =                         = */
/* =========================== */

import { error as logError } from '@tauri-apps/plugin-log'
import { exitDeskset } from './main/tauri'

const isDevEnv = (import.meta as any).env.DEV as boolean


/* ==== 启动服务器 ==== */
import { spawnServer, axios } from './global'

let isSpawn = true

try {
  // 运行 DesksetBack.exe 桌设后端服务器进程
  const serverInfo = await spawnServer()

  // Manager 设置 axios 参数
  axios.defaults.baseURL = `http://${serverInfo.url}`
  axios.defaults.headers.common['Authorization'] = `Bearer ${serverInfo.token}`

  // Manager 向 Desktop 发送 axios 参数
  const broadcast = new BroadcastChannel('axios')
  broadcast.postMessage({url: serverInfo.url, token: serverInfo.token})
} catch (err) {
  isSpawn = false
  logError('Spawn DesksetBack Fail')
}

// 开发环境：无需考虑服务器是否启动成功
if (isDevEnv) {
  isSpawn = true
  axios.defaults.baseURL = 'http://127.0.0.1:6527'
}


/* ==== 加载配置 ==== */
import { config } from './global'
import { readConfFile } from './main/config'
import { isEnabled } from '@tauri-apps/plugin-autostart'

config.isAutostart = await isEnabled()  // 是否注册开机启动

try {
  let timeout = 1000
  if (isDevEnv) timeout = 100  // 开发环境可能没有启动服务器，缩短超时时间，加快 main 加载速度
  config.server_port = (await axios.get('/v0/config/server-port', { timeout: timeout })).data.result
  config.username = (await axios.get('/v0/config/username', { timeout: timeout })).data.result
  config.password = (await axios.get('/v0/config/password', { timeout: timeout })).data.result
} catch {}

// 读取文件中的配置/持久化配置
const conf = await readConfFile()
config.language = conf.language
config.closeBehavior = conf.closeBehavior

// - [ ] 临时：切换 _t 翻译语言...
import { switchLanguage } from './main/i18n'

await switchLanguage(config.language)


/* ==== 监听主进程 ==== */
import { listen } from '@tauri-apps/api/event'

listen('quit', async () => {
  await exitDeskset()
})


/* ==== 监听管理窗口 ==== */
import winManager from './global/win/manager'

winManager.onCloseRequested(async (event) => {
  event.preventDefault()

  if (config.closeBehavior == 'hide' && isSpawn == true) {
    await winManager.hide()
  } else {
    await exitDeskset()
  }
})


/* ==== 监听桌面页面 ==== */
import { activeWidgetMap } from './global'

const broadcast = new BroadcastChannel('DesktopSend')

// - [ ] 优化？防抖节流 & 新开线程
broadcast.onmessage = (ev) => {
  const data = ev.data
  const widget = activeWidgetMap.get(data.id)
  if (widget != undefined) {
    if (data.model) {
      widget.model = data.model
    } else {
      widget!.x = data.x
      widget!.y = data.y
      widget!.left = data.left
      widget!.top = data.top
    }
  } else {
    // 小概率：桌面页 mount 完毕，但是管理页还未 set
    console.log(`Desktop send ${data.id} before Manager set`)
  }
}


/* ==== 加载部件、主题 ==== */
import { activeThemeMap, LATEST_THEME_ROOT, LATEST_THEME_NAME } from './global'
import { _getThemes, _applyTheme } from './main/theme'

// 读取主题库
const themes = await _getThemes()
for (const theme of themes) {
  activeThemeMap.set(theme.name, theme)
}

// 应用上次关闭时的主题
try {
  await _applyTheme(LATEST_THEME_NAME, LATEST_THEME_ROOT)
} catch (err) {
  logError(`Fail to apply ${LATEST_THEME_ROOT}/${LATEST_THEME_NAME} theme(latest widget list), error: ${err}`)
}


/* ==== 应用 ==== */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Manager from './Manager.vue'

const app = createApp(Manager)
  .use(router)
  .provide('$axios', axios)
  .provide('$isSpawn', isSpawn)
  .use(createPinia())
  .mount('#manager')
