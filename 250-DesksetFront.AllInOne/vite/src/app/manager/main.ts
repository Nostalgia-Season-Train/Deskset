import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

// - [ ] 测试部件管理的功能
import { WidgetChannel } from '@src/shared/global'
import { WidgetManagerClient } from '@src/feature/widget/manager'

const widgetManagerClient = new WidgetManagerClient(WidgetChannel)
widgetManagerClient.appendWidget('datetime/clock', true)
