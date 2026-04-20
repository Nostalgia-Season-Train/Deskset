import { TrayIcon } from '@tauri-apps/api/tray'
import { defaultWindowIcon } from '@tauri-apps/api/app'
import { Menu } from '@tauri-apps/api/menu'
import winManager from '#manager/global/win/manager.ts'
import { exitDeskset } from './tauri.ts'

export const tray = await TrayIcon.new({
  tooltip: 'Deskset',
  icon: await defaultWindowIcon() as any,
  showMenuOnLeftClick: false,
  menu: await Menu.new({
    items: [{
      id: 'show',
      text: '显示',
      action: async () => await winManager.show()
    }, {
      id: 'quit',
      text: '退出',
      action: async () => await exitDeskset()
    }]
  })
})

// F5 刷新 Vue 界面时，关闭托盘
window.addEventListener('beforeunload', async () => {
  await tray.close()
})
