/* ==== 是否非空（非 null 非 undefined） ==== */
export function isNotEmpty(value: any): boolean {
  return value !== null && value !== undefined
}


/* ==== 重置网页默认行为 ==== */
export function resetDefault() {
  // 刷新和开发者工具
  document.addEventListener('keydown', (event: KeyboardEvent) => {
    if (
      event.key === 'F5' ||  // F5 刷新
      (event.ctrlKey && event.key === 'r') ||  // Windows/Linux 上：Ctrl + R 刷新
      (event.metaKey && event.key === 'r') ||  // Mac 上：Command + R 刷新
      event.key === 'F12' ||  // F12 开发者工具
      (event.ctrlKey && event.key === 'f')  // Ctrl + F 搜索
    ) {
      event.preventDefault()
    }
  })
  // 右键菜单
  document.addEventListener('contextmenu', (event: MouseEvent) => {
    event.preventDefault()
  })
}
