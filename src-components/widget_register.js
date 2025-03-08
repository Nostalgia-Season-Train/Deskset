/* === 导入组件 === */
const rawComponents = import.meta.glob("./*/*.vue")

// 按中文排序
const sortKeys = Object.keys(rawComponents).sort((a, b) => a.localeCompare(b, 'zh-CN'))
const sortDict = sortKeys.reduce((add, key) => {
  add[key] = rawComponents[key]
  return add
}, {})
const components = sortDict


/* === 遍历组件 === */
let categoryList = new Map()
let widgetList = []
let num = 0

for (const path in components) {
  const path_parts = path.replace(".vue", "").split("/").slice(1)

  const id = path_parts.join("/")  // 组件 ID = 类型/名称 - 文件夹/文件名
  const category = path_parts[0]   // 类型 - 文件夹
  const name     = path_parts[1]   // 名称 - 文件名

  if (!categoryList.has(category)) {
    categoryList.set(category, [])
  }
  categoryList.get(category).push(name)

  widgetList.push({
    num: num,  // 临时给一些简单遍历场景提供索引
    id:       id,
    category: category,
    name:     name,
    content: components[path],
    isDisplay: false
  })

  num++
}


/* === 导出组件 === */
export const categorys = categoryList
export const widgets = widgetList
export const number = num
