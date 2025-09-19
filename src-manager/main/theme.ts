import {
  readDir,
  mkdir,
  readTextFile,
  writeTextFile,
  remove,
  BaseDirectory
} from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'
import desktop from '#manager/global/page/desktop'
import { Theme, activeThemeMap, LATEST_THEME } from '#manager/global/theme.ts'  // #manager/global 找不到类型声明？原因？
import {
  activeWidgetMap,
  activeWidgetOnSelect,
  convertWidgetInTheme
} from '#manager/global/widget'


/* === 遍历主题 === */
export const _getThemes = async () => {
  const entrys = await readDir('./themes', { baseDir: BaseDirectory.Resource })

  let themes: Theme[] = []
  for (const entry of entrys) {
    try {
      if (entry.isDirectory == false)
        continue
      const name = entry.name
      const infoText = await readTextFile(`./themes/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })
      const info = JSON.parse(infoText)
      themes.push({
        name: name,
        savetime: info?.savetime ?? '',
        descript: info?.descript ?? ''
      })
    } catch (err) {
      logError(`Get ${entry.name} theme fail, error: ${err}`)
    }
  }
  return themes
}


/* === 保存主题 === */
import dayjs from 'dayjs'

export const _saveTheme = async (name: string) => {
  // 数据转换 + 信息生成
  const data = {
    window: await desktop.getWindowData(),
    widgets: (
      await Promise.all([...activeWidgetMap.values()].map(convertWidgetInTheme))
    ).filter(widget => widget != undefined)  // 转换失败的元素返回 undefined
  }
  const info = {
    savetime: String(dayjs().format('YYYY-MM-DD HH:mm:ss')),
    descript: ''
  }

  // 写入文件
  const dataText = JSON.stringify(data, null, 2)
  const infoText = JSON.stringify(info, null, 2)
  await mkdir(`./themes/${name}`, { baseDir: BaseDirectory.Resource, recursive: true })
  await writeTextFile(`./themes/${name}/data.json`, dataText, { baseDir: BaseDirectory.Resource })
  await writeTextFile(`./themes/${name}/metainfo.json`, infoText, { baseDir: BaseDirectory.Resource })

  // 加入列表
  activeThemeMap.set(name, {
    name: name,
    savetime: info.savetime,
    descript: info.descript
  })
}


/* === 删除主题 === */
export const _deleteTheme = async (name: string) => {
  await remove(`./themes/${name}`, { baseDir: BaseDirectory.Resource, recursive: true })
  activeThemeMap.delete(name)
}


/* === 应用主题 === */
import { appendWidget } from './widget'

export const _applyTheme = async (name: string) => {
  // 读取主题数据
  const dataText = await readTextFile(`./themes/${name}/data.json`, { baseDir: BaseDirectory.Resource })
  const data = JSON.parse(dataText)

  // 移除桌面上的部件 + 部件列表清空 + 部件选中重置
  for (const widget of [...activeWidgetMap.values()]) {
    await desktop.removeWidget(widget.id)
  }
  activeWidgetMap.clear()
  activeWidgetOnSelect.value = null

  // 重新挨个添加部件
  for (const widgetInThemeFile of data.widgets) {
    const widgetInTheme = await convertWidgetInTheme(widgetInThemeFile)
    if (widgetInTheme == undefined)
      continue

    await appendWidget(widgetInTheme)
  }
}


/* ==== [ ] 测试中 Pinia ==== */
import { defineStore } from 'pinia'
import { computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const themes = computed({
    get() {
      return Array.from(activeThemeMap.values()).filter((item: Theme) => item.name != LATEST_THEME)
    },
    set() {}
  })

  const saveTheme = _saveTheme
  const deleteTheme = _deleteTheme
  const applyTheme = _applyTheme

  return { themes, saveTheme, deleteTheme, applyTheme }
})
