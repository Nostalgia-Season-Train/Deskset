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
