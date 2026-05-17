// 是否为 Vite 开发环境
export const DEVELOP_ENV = import.meta.env.DEV
// 是否为 Tauri 运行时（在 Tauri 窗口上显示）
export const TAURI_RUNTIME = (window as any).__TAURI_INTERNALS__ !== undefined
