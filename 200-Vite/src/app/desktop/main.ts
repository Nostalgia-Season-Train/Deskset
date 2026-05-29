/* ==== 静态样式 ==== */
import 'element-plus/dist/index.css'
import './style.less'


/* ==== Vue 应用 ==== */
import { createApp } from 'vue'
import App from './App.vue'

// - [ ] 测试部件管理的功能
const app = createApp(App).mount('#app')

import { WidgetChannel } from '@src/shared/global'
import { inlineWidgetclsMap } from '@src/app/widget/register'
import { WidgetManagerServer } from '@src/feature/deskbeauty/widget/manager'

// @ts-expect-error
const widgetManagerServer =
  new WidgetManagerServer(
    WidgetChannel,
    inlineWidgetclsMap,
    app.$el
  )
