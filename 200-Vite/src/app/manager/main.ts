/* ==== 静态样式 ==== */
import 'element-plus/dist/index.css'
import './style.less'


/* ==== Vue 应用 ==== */
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

// - [ ] 测试部件管理的功能
import { WidgetChannel } from '@src/shared/global'
import { WidgetManagerClient } from '@src/feature/deskbeauty/widget/manager'

const widgetManagerClient = new WidgetManagerClient(WidgetChannel)
widgetManagerClient.appendWidget('datetime/clock', true)
