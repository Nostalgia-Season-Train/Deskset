import { reactive } from 'vue'

export interface Theme {
  // 主题名称 = 主题 ID = 主题目录
  name: string

  // 主题信息 metainfo
  savetime: string
  descript: string
}

export const activeThemeMap = reactive(new Map<string, Theme>())
