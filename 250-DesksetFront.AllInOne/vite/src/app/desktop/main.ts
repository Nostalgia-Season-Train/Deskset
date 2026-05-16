import { createApp } from 'vue'
import App from './App.vue'

// - [ ] 测试部件管理的功能
const app = createApp(App).mount('#app')

import { WidgetChannel } from '@src/shared/global'
import { inlineWidgetclsMap } from '@src/app/widget/register'
import { WidgetManagerServer } from '@src/feature/widget/manager'

// @ts-expect-error
const widgetManagerServer =
  new WidgetManagerServer(
    WidgetChannel,
    inlineWidgetclsMap,
    app.$el
  )
