export const sortList = async (rawList: any[], rawSorts: any[]) => {
  // 优先排序在后，覆盖在前的次要排序
  const sorts = rawSorts.toReversed()
  // Obsidian 数据库的隐式排序...
  const list = rawList.sort((a: any, b: any) => {
    return a['file.fullname'].localeCompare(b['file.fullname'], 'zh-cn')
  })

  // 排序
  for (const sort of sorts) {
    list.sort((a: any, b: any) => {
      // 属性键不区分大小写
      const aValue = a[sort.dataKey.toLowerCase()]
      const bValue = b[sort.dataKey.toLowerCase()]
      // 相同，顺序不变
      if (aValue === bValue)
        return 0
      // 键不存在
      if (aValue === undefined && bValue !== undefined)
        return 1
      if (aValue !== undefined && bValue === undefined)
        return -1
      // 值不存在
      if (aValue === null && bValue !== null)
        return 1
      if (aValue !== null && bValue === null)
        return -1
      const compare = (m: any, n: any) => {
        if (typeof m !== 'boolean' && typeof n === 'boolean')
          return 1
        if (typeof m === 'boolean' && typeof n !== 'boolean')
          return -1
        if (typeof m === 'boolean' && typeof n === 'boolean')
          return m < n ? -1 : 1
        // 比较数字
        if (typeof m !== 'number' && typeof n === 'number')
          return 1
        if (typeof m === 'number' && typeof n !== 'number')
          return -1
        if (typeof m === 'number' && typeof n === 'number')
          return m < n ? -1 : 1
        // 比较字符串
        if (typeof m === 'string' && typeof n === 'string')
          return m.localeCompare(n, 'zh-cn')
        // 鬼知道这是啥
        return 0
      }
      if (sort.direct === 'asc')
        return compare(aValue, bValue)
      else
        return -compare(aValue, bValue)
    })
  }

  return list
}
