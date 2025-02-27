// 桌面页面 pageDesktop 在桌面窗口 winDesktop 上显示
const pageDesktop = new BroadcastChannel('pageDesktop')
const winDesktop = window.winDesktop


const desktop = {
  /* === 组件 === */
  getWidgetOnDesktop: async (widgetId) => pageDesktop.postMessage({
    'action': 'getWidgetOnDesktop',
    'id': widgetId,
  }),

  // 组件控制
  switchDisplay: async (widgetId, isDisplay) => pageDesktop.postMessage({
    'action': 'switchDisplay',
    'id': widgetId,
    'isDisplay': isDisplay
  }),
  switchProp: async (id, prop, is) => pageDesktop.postMessage({
    action: 'switchProp', id: id, prop: prop, is: is
  }),

  /* === 主题 === */
  saveTheme: async (themeName) => pageDesktop.postMessage({
    'action': 'saveTheme',
    'themeName': themeName
  }),
  useTheme: async (themeName) => pageDesktop.postMessage({
    'action': 'useTheme',
    'themeName': themeName
  }),

  /* === 开发 === */
  refresh: async () => pageDesktop.postMessage({ 'action': 'refreshPage' }),
  openDevTool: async () => winDesktop.openDevTool()
}


export default desktop
