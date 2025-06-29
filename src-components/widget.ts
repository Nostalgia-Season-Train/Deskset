/* === 导入组件 === */
const rawComponents = import.meta.glob('./*/*.vue')

// 按照中文排序
const sortKeys = Object.keys(rawComponents).sort((a, b) => a.localeCompare(b, 'zh-CN'))
const sortDict = sortKeys.reduce((add: any, key: string) => {
  add[key] = rawComponents[key]
  return add
}, {})
const sortRawComponents = sortDict


/* === 遍历组件，生成部件 === */
const widget = new Map<string, {
  local: string  // 位置 = 分类/名称 - 文件夹/文件
  type: string   // 分类 - 文件夹
  name: string   // 名称 - 文件
  content: string
}>()

for (const cpath in sortRawComponents) {  // cpath：以部件库（目前是 src-components）为根目录的相对路径
  const cpathParts = cpath.replace('.vue', '').split('/').slice(1)

  const local = cpathParts.join('/')
  const type = cpathParts[0]
  const name = cpathParts[1]

  widget.set(local, {
    local: local,
    type: type,
    name: name,
    content: sortRawComponents[cpath]
  })
}


/* === 导出部件 === */
export const rawWidgetMap = widget
