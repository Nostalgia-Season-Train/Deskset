import { defineStore } from 'pinia'
import { computed } from 'vue'
import { activeThemeMap } from './mvar'
import { _saveTheme, _deleteTheme, _applyTheme } from './mfunc'

export const useThemeStore = defineStore('theme', () => {
  const themes = computed({
    get() {
      return Array.from(activeThemeMap.values())
    },
    set() {}
  })

  async function saveTheme(name: string) {
    return await _saveTheme(name)
  }
  async function deleteTheme(name: string) {
    return await _deleteTheme(name)
  }
  async function applyTheme(name: string) {
    return await _applyTheme(name)
  }

  return { themes, saveTheme, deleteTheme, applyTheme }
})
