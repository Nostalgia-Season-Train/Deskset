// @ts-nocheck
import dayjs from 'dayjs'

export const prefixMark = '/@Deskset/'

export const inlineRawWidgetMap = new Map([
  /* --- 笔记 --- */
  [`${prefixMark}Base`, {
    main: () => import('/src-widget/note/base.vue'),
    metainfo: await import('/src-widget/note/base.json')
  }],
  [`${prefixMark}NumStats`, {
    main: () => import('/src-widget/note/num-stats.vue'),
    metainfo: await import('/src-widget/note/num-stats.json')
  }],
  [`${prefixMark}Diary`, {
    main: () => import('/src-widget/note/diary.vue'),
    metainfo: await import('/src-widget/note/diary.json')
  }],
  [`${prefixMark}Heatmap`, {
    main: () => import('/src-widget/note/heatmap.vue'),
    metainfo: await import('/src-widget/note/heatmap.json')
  }],
  [`${prefixMark}VaultStatus`, {
    main: () => import('/src-widget/note/vault-status.vue'),
    metainfo: await import('/src-widget/note/vault-status.json')
  }],

  /* --- 时间和日期 --- */
  [`${prefixMark}Clock`, {
    main: () => import('/src-widget/datetime/clock.vue'),
    metainfo: await import('/src-widget/datetime/clock.json')
  }],
  [`${prefixMark}Calendar`, {
    main: () => import('/src-widget/datetime/calendar.vue'),
    metainfo: await import('/src-widget/datetime/calendar.json')
  }],
  [`${prefixMark}Stopwatch`, {
    main: () => import('/src-widget/datetime/stopwatch.vue'),
    metainfo: await import('/src-widget/datetime/stopwatch.json')
  }],
  [`${prefixMark}Timer`, {
    main: () => import('/src-widget/datetime/timer.vue'),
    metainfo: await import('/src-widget/datetime/timer.json')
  }],
  [`${prefixMark}DateCounter`, {
    main: () => import('/src-widget/datetime/date-counter.vue'),
    metainfo: await import('/src-widget/datetime/date-counter.json')
  }],

  /* --- 设备信息 --- */
  [`${prefixMark}HardwareMonitor`, {
    main: () => import('/src-widget/device/hardware-monitor.vue'),
    metainfo: await import('/src-widget/device/hardware-monitor.json')
  }],
  [`${prefixMark}DiskStorage`, {
    main: () => import('/src-widget/device/disk-storage.vue'),
    metainfo: await import('/src-widget/device/disk-storage.json')
  }],
  [`${prefixMark}Battery`, {
    main: () => import('/src-widget/device/battery.vue'),
    metainfo: await import('/src-widget/device/battery.json')
  }],
])

export const inlineWidgetList = [...inlineRawWidgetMap.keys()]

// ** 搜索嵌套目录（包括当前目录）
// *  搜索一级子目录
const rawWidgetCode = import.meta.glob('./*/*.vue')                          // 部件代码（Vue SFC 文件）
const rawWidgetInfo = import.meta.glob('./*/*.json', { import: 'default' })  // 部件信息

let _inlineWidgetclsMap = new Map()  // 备选名：部件模板、部件蓝图
for (const [rawPath, rawMain] of Object.entries(rawWidgetCode)) {
  // 去掉 ./ 和 .vue 前后缀
  const path = rawPath.slice(2, -4)
  // 部件代码要有对应的部件信息，否则跳过
  const importRawInfo = rawWidgetInfo[`./${path}.json`]
  if (importRawInfo === undefined)
    continue
  // 添加部件类
  _inlineWidgetclsMap.set(path, {
    main: rawMain,
    path: path,
    beInline: true,
    ...(await importRawInfo())
  })
}
export const inlineWidgetclsMap = _inlineWidgetclsMap
