/* ==== 静态样式 ==== */
import './style.less'


/* ==== Vue 应用 ==== */
import { createApp } from 'vue'
import App from './App.vue'

// - [ ] 测试部件管理的功能
const app = createApp(App).mount('#app')

const WidgetChannel = new BroadcastChannel('Widget')
import { inlineWidgetclsMap } from './widget/register'
import { WidgetManagerServer } from '@deskset/deskbeauty'

// @ts-expect-error
const widgetManagerServer =
  new WidgetManagerServer(
    WidgetChannel,
    inlineWidgetclsMap,
    app.$el
  )
