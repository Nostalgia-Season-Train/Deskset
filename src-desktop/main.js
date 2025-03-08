import { createApp } from 'vue'
import './style.css'

import ElementPlus from 'element-plus'
import zh_CN from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'

import 'echarts'

import Desktop from './Desktop.vue'
import drag from './widgetDrag'

import '../static/css/default-font.css'


const app = createApp(Desktop)

app.use(ElementPlus, { locale: zh_CN })
app.use(drag)
app.mount('#desktop')
