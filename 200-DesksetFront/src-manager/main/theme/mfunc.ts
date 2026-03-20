import {
  readDir,
  mkdir,
  readTextFile,
  writeTextFile,
  writeFile,
  remove,
  BaseDirectory
} from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'
import desktop from '#manager/main/desktop.ts'
import { Theme, activeThemeMap, THEME_LIB, LATEST_THEME_ROOT, LATEST_THEME_NAME } from './mvar'  // #manager/global 找不到类型声明？原因？
import { activeWidgetMap, activeWidgetOnSelect } from '#manager/main/widget/mvar'


/* === 遍历主题 === */
export const _getThemes = async (root: string = THEME_LIB) => {
  const entrys = await readDir(`./${root}`, { baseDir: BaseDirectory.Resource })

  let themes: Theme[] = []
  for (const entry of entrys) {
    try {
      if (entry.isDirectory == false)
        continue
      const name = entry.name
      const infoText = await readTextFile(`./${root}/${name}/metainfo.json`, { baseDir: BaseDirectory.Resource })
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
import { RuntimeToStorageWidget } from '#manager/main/widget/mfunc'

export const _saveTheme = async (name: string, root: string = THEME_LIB) => {
  // 数据转换 + 信息生成
  const data = {
    window: await desktop.getWindowData(),
    widgets: (await Promise.all([...activeWidgetMap.values()].map(RuntimeToStorageWidget)))
  }
  const info = {
    savetime: String(dayjs().format('YYYY-MM-DD HH:mm:ss')),
    descript: ''
  }

  // 写入文件
  const dataText = JSON.stringify(data, null, 2)
  const infoText = JSON.stringify(info, null, 2)
  await mkdir(`./${root}/${name}`, { baseDir: BaseDirectory.Resource, recursive: true })
  await writeTextFile(`./${root}/${name}/data.json`, dataText, { baseDir: BaseDirectory.Resource })
  await writeTextFile(`./${root}/${name}/metainfo.json`, infoText, { baseDir: BaseDirectory.Resource })

  // 保存桌面窗口预览（截图）
  const arrayPicture = await desktop.getWindowPicture()
  await writeFile(`./${root}/${name}/preview.png`, new Uint8Array(arrayPicture), { baseDir: BaseDirectory.Resource })

  // 加入列表
  activeThemeMap.set(name, {
    name: name,
    savetime: info.savetime,
    descript: info.descript
  })
}

// 退出时保存这次桌面主题
export const saveLatestTheme = async () => {
  await _saveTheme(LATEST_THEME_NAME, LATEST_THEME_ROOT)
}


/* === 删除主题 === */
export const _deleteTheme = async (name: string, root: string = THEME_LIB) => {
  await remove(`./${root}/${name}`, { baseDir: BaseDirectory.Resource, recursive: true })
  activeThemeMap.delete(name)
}


/* === 应用主题 === */
import { appendWidget } from '#manager/main/widget/mfunc'
import { FileToStorageWidget } from '#manager/main/widget/mfunc'

export const _applyTheme = async (name: string, root: string = THEME_LIB) => {
  // 读取主题数据
  const dataText = await readTextFile(`./${root}/${name}/data.json`, { baseDir: BaseDirectory.Resource })
  const data = JSON.parse(dataText)

  // 移除桌面上的部件 + 部件列表清空 + 部件选中重置
  for (const widget of [...activeWidgetMap.values()]) {
    await desktop.removeWidget(widget.id)
  }
  activeWidgetMap.clear()
  activeWidgetOnSelect.value = null

  // 重新挨个添加部件
  for (const fileWidget of data.widgets) {
    const storageWidget = await FileToStorageWidget(fileWidget)
    if (storageWidget == undefined)
      continue

    await appendWidget(storageWidget)
  }
}

// 启动时应用上次桌面主题
export const applyLatestTheme = async () => {
  await _applyTheme(LATEST_THEME_NAME, LATEST_THEME_ROOT)
}
