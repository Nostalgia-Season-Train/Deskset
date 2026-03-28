// ** 搜索嵌套目录（包括当前目录）
// *  搜索一级子目录
const rawWidgetCode = import.meta.glob('./*/*.vue')                          // 部件代码（Vue SFC 文件）
const rawWidgetInfo = import.meta.glob('./*/*.json', { import: 'default' })  // 部件信息

const registerList = [
  /* --- 笔记 --- */
  './note/base.vue',
  './note/num-stats.vue',
  './note/diary.vue',
  './note/heatmap.vue',
  './note/vault-status.vue',
  /* --- 时间和日期 --- */
  './datetime/clock.vue',
  './datetime/calendar.vue',
  './datetime/stopwatch.vue',
  './datetime/timer.vue',
  './datetime/date-counter.vue',
  /* --- 设备信息 --- */
  './device/hardware-monitor.vue',
  './device/disk-storage.vue',
  './device/battery.vue',
]
let rawWidgetCodeSort = Object.create(null)
for (const rawPath of registerList) {
  if (rawPath in rawWidgetCode)
    rawWidgetCodeSort[rawPath] = rawWidgetCode[rawPath]
}

let _inlineWidgetclsMap = new Map()  // 备选名：部件模板、部件蓝图
for (const [rawPath, rawMain] of Object.entries(rawWidgetCodeSort)) {
  // 去掉 ./ 和 .vue 前后缀
  const path = rawPath.slice(2, -4)
  // 部件代码要有对应的部件信息，否则跳过
  const importRawInfo = rawWidgetInfo[`./${path}.json`]
  if (importRawInfo === undefined)
    throw Error(`部件代码 ${rawPath} 没有对应的部件信息`)  // 显式报错提醒
  // 添加部件类
  _inlineWidgetclsMap.set(path, {
    main: rawMain,
    path: path,
    beInline: true,
    // @ts-ignore
    ...(await importRawInfo())
  })
}
export const inlineWidgetclsMap = _inlineWidgetclsMap
