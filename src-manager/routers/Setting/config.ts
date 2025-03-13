/* === Update 配置 === */
import { ref, toRaw, watch } from 'vue'
import { readFile, writeFile, BaseDirectory } from '@tauri-apps/plugin-fs'

const confUpdatePath = 'config/update.json'

export const confUpdate = ref({  // 默认配置
  AutoUpdate: true,      // 自动更新
  VersionType: 'Stable'  // 版本类型：稳定版 Stable、预览版 Preview
})

// 读取配置，没有则创建
const getConfigUpdate = async () => {
  try {
    const confUpdateFile = await readFile(`./${ confUpdatePath }`, { baseDir: BaseDirectory.Resource })
    confUpdate.value = JSON.parse(new TextDecoder().decode(confUpdateFile))
  } catch {
    setConfigUpdate()
  }
}
getConfigUpdate()  // 只有 import config.ts 时才会执行

// 写入配置
const setConfigUpdate = async () => { 
  const encoder = new TextEncoder()
  const confUpdateFile = encoder.encode(JSON.stringify(toRaw(confUpdate.value), null, 4))
  writeFile(`./${ confUpdatePath }`, confUpdateFile, { baseDir: BaseDirectory.Resource })
}

// 监测 confUpdate 变化
watch(confUpdate, async (newval, oldval) => {
  setConfigUpdate()
}, { deep: true })  // deep: true：ref(Object) 中 Object 属性变化也能触发 watch
