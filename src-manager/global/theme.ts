import { reactive } from 'vue'

export interface Theme {
  // 主题名称 = 主题 ID = 主题目录
  name: string

  // 主题信息 metainfo
  savetime: string
  descript: string
}

export const activeThemeMap = reactive(new Map<string, Theme>())

export const THEME_LIB = 'themes'

// 应用关闭时，将当前桌面保存为主题存放在 LATEST_THEME_ROOT/LATEST_THEME_NAME 文件夹中
export const LATEST_THEME_ROOT = 'config'
export const LATEST_THEME_NAME = 'theme/latest'
