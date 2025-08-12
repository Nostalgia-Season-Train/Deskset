import { error as logError } from '@tauri-apps/plugin-log'
import { BaseDirectory } from '@tauri-apps/plugin-fs'
import { StorageConf, config } from '#manager/global/config'


/* === 读取（持久化）配置 === */
import { readTextFile } from '@tauri-apps/plugin-fs'

export const readConfFile = async (): Promise<StorageConf> => {
  let storageConf: StorageConf = {
    closeBehavior: config.closeBehavior
  }

  try {
    const conf = JSON.parse(await readTextFile('./config/deskset.json', { baseDir: BaseDirectory.Resource }))

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
