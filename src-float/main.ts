/* 导入默认字体 */
import '../static/css/default-font.css'

/* 创建 Vue 应用 */
import { createApp } from 'vue'
import './style.css'

import Float from './Float.vue'

const app = createApp(Float)
  .mount('#float')
