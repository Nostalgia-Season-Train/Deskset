import { createApp } from 'vue'
import './style.css'

import 'element-plus/dist/index.css'  // Element Plus 样式由桌面提供

import Desktop from './Desktop.vue'
import drag from './widgetDrag'

import '../static/css/default-font.css'


const app = createApp(Desktop)

app.use(drag)
app.mount('#desktop')
