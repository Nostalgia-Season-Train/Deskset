import { error as logError } from '@tauri-apps/plugin-log'
import { BaseDirectory } from '@tauri-apps/plugin-fs'
import { StorageConf, config } from '#manager/global/config'


/* === 读取（持久化）配置 === */
import { readTextFile } from '@tauri-apps/plugin-fs'

export const readConfFile = async (): Promise<StorageConf> => {
  let storageConf: StorageConf = {
    language: config.language,
    closeBehavior: config.closeBehavior
  }

  try {
    const conf = JSON.parse(await readTextFile('./config/deskset.json', { baseDir: BaseDirectory.Resource }))

    if (conf.language == 'zh-cn' || 'en') {
      storageConf.language = conf.language
    }
    if (conf.closeBehavior == 'hide' || 'exit') {
      storageConf.closeBehavior = conf.closeBehavior
    }
  } catch (err) {
    logError(`Fail to read conf, error: ${err}`)
  }

  return storageConf
}


/* === 写入（持久化）配置 === */
import { writeTextFile } from '@tauri-apps/plugin-fs'

export const writeConfFile = async (conf: StorageConf) => {
  try {
    await writeTextFile('./config/deskset.json', JSON.stringify(conf, null, 2), { baseDir: BaseDirectory.Resource })
  } catch (err) {
    logError(`Fail to write conf, error: ${err}`)
  }
}


/* ==== [ ] 测试中 Pinia ==== */
import { defineStore } from 'pinia'
import { computed } from 'vue'
import axios from 'axios'
import { enable, disable, isEnabled } from '@tauri-apps/plugin-autostart'

export const useConfigStore = defineStore('config', () => {
  const language = computed({
    get() {
      // 必需加上 as string 不然 TypeScript 语言服务器无法识别 language 类型
      return config.language as string
    },
    async set(value) {
      // 设置 Deskset 语言
      if (value == 'zh-cn')
        config.language = 'zh-cn'
      else
        config.language = 'en'
      // 设置 DesksetBack 语言
      try {
        await axios.post(
          '/v0/config/language',
          new URLSearchParams({ language: config.language }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          }
        )
      } catch {}
    }
  })

  const isAutostart = computed({
    get() {
      return config.isAutostart as boolean
    },
    async set(value) {
      if (value)
        await enable()
      else
        await disable()
      config.isAutostart = await isEnabled()
    }
  })

  const closeBehavior = computed({
    get() {
      return config.closeBehavior as string
    },
    set(value) {
      if (value == 'hide')
        config.closeBehavior = 'hide'
      else
        config.closeBehavior = 'exit'
    }
  })

  return { language, isAutostart, closeBehavior }
})
