/* ==== 静态样式 ==== */
import './style.less'
import 'element-plus/dist/index.css'

/* ==== Vue 应用 ==== */
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './main/router'

const app = createApp(App)
app.use(router)
app.mount('#app')
