import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// === 全局变量 ===
// @ts-expect-error process is a nodejs global
const host = process.env.TAURI_DEV_HOST;


// === vite 配置 ===
export default defineConfig(async () => ({
  base: './',
  build: {
    outDir: path.resolve(__dirname, './dist'),
    emptyOutDir: true,  // 清空上次构建
    rollupOptions: {
      input: {
        // manager 管理组件；desktop 放置组件
        manager: path.resolve(__dirname, 'manager.html'),
        desktop: path.resolve(__dirname, 'desktop.html'),
        float: path.resolve(__dirname, 'float.html')
      }
    },
    target: 'es2022'  // 支持顶级 await 的环境，使用 await 时不用 async 包裹
  },

  plugins: [vue()],

  // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
  //
  // 1. prevent vite from obscuring rust errors
  clearScreen: false,
  // 2. tauri expects a fixed port, fail if that port is not available
  server: {
    port: 1420,
    strictPort: true,
    host: host || false,
    hmr: host
      ? {
          protocol: "ws",
          host,
          port: 1421,
        }
      : undefined,
    watch: {
      // 3. tell vite to ignore watching `src-tauri`
      ignored: ["**/src-tauri/**"],
    },
  },
}));
