import { WebviewWindow } from '@tauri-apps/api/webviewWindow'
import { Effect } from '@tauri-apps/api/window'
import axios from 'axios'

class FloatManager {
  private floatList: Map<string, WebviewWindow>

  constructor() {
    this.floatList = new Map()
  }

  create = async (page: string, width: number, height: number, alwaysOnTop: boolean = true) => {
    const url = axios.defaults.baseURL ?? ''
    const token = axios.defaults.headers.common['Authorization']?.toString().slice(7) ?? ''
    const floatWin = new WebviewWindow(`float:${page}`, {
      url: `float.html#/${page}?url=${url}&token=${token}`,
      title: `Deskset Float ${page}`,
      transparent: true, decorations: false, shadow: false, skipTaskbar: true,
      windowEffects: { effects: [Effect.Blur] },
      alwaysOnTop: alwaysOnTop,
      x: 100, y: 100,
      width: width, height: height,
      resizable: false,
      maximizable: false  // 避免双击最大化
    })
    await floatWin.once('tauri://error', async (error: any) => { console.log(error) })
    await floatWin.show()

    this.floatList.set(page, floatWin)
  }

  close = async (page: string) => {
    const window = this.floatList.get(page)
    await window?.close()
    // 二次关闭
    setTimeout(async () => {
      const window = this.floatList.get(page)
      if (window === undefined)
        return
      console.log(`关闭 ${page} 失败，再次关闭！当前浮动窗口列表：\n`, this.floatList)
      await window.close()
    }, 300)
  }

  closeAll = async () => {
    for (const [_, window] of this.floatList) {
      await window.close()
    }
  }
}

export const floatManager = new FloatManager()


/* ==== Pinia ==== */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFloatStore = defineStore('float', () => {
  let hasDiary = ref(false)
  const diary = computed({
    get() {
      return hasDiary.value
    },
    async set(v: boolean) {
      try {
        if (v === true && hasDiary.value === false) {
          hasDiary.value = true
          await floatManager.create('Diary', 240, 160)
        }
        else if (v === false && hasDiary.value === true) {
          hasDiary.value = false
          await floatManager.close('Diary')
        }
      } catch { }
    }
  })

  return { diary }
})
