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
  [`${prefixMark}Stopwatch`, {
    main: () => import('/src-widget/datetime/stopwatch.vue'),
    metainfo: await import('/src-widget/datetime/stopwatch.json')
  }],

  /* --- 时间与日期 --- */
  [`${prefixMark}FlipClock`, {
    // @ts-ignore
    main: () => import('/src-widget/时间与日期/翻页时钟.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '以 HHmmss 格式，显示现在时间',
      model: {
        top_bgcolor: '#212121',
        bottom_bgcolor: '#757575'
      },
      options: [{
        name: '上半部分颜色',
        type: 'ColorPicker',
        key: 'top_bgcolor'
      }, {
        name: '下半部分颜色',
        type: 'ColorPicker',
        key: 'bottom_bgcolor'
      }]
    }
  }],
  [`${prefixMark}Countdown`, {
    // @ts-ignore
    main: () => import('/src-widget/时间与日期/倒计时.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '计算距离某天某时还剩多久',
      model: {
        title: `距离 ${dayjs().add(1, 'day').format('YYYY-MM-DD')} 还剩`,
        deadline: async () => { return Number(new Date().setDate(new Date().getDate() + 1)) }
      },
      options: [{
        name: '标题',
        type: 'Input',
        key: 'title'
      }, {
        name: '截止日期',
        type: 'DateTimePicker',
        key: 'deadline'
      }]
    }
  }],

  /* --- 个性资料、问候语 --- */
  [`${prefixMark}Greeting`, {
    // @ts-ignore
    main: () => import('/src-widget/问候语/打字机问候.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '根据当前时段，显示个性化问候语'
    }
  }],

  /* --- 硬件监控 --- */
  [`${prefixMark}RealtimeMonitoring`, {
    // @ts-ignore
    main: () => import('/src-widget/硬件监控/实时监控.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '查看芯片和内存的占用率'
    }
  }],
  [`${prefixMark}DiskCapacity`, {
    // @ts-ignore
    main: () => import('/src-widget/硬件监控/硬盘容量.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '展示所有硬盘分区剩余容量和总存储空间'
    }
  }],
  [`${prefixMark}BatteryPower`, {
    // @ts-ignore
    main: () => import('/src-widget/硬件监控/电池电量.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '显示电脑电池剩余电量，是否正在充电'
    }
  }],
])

export const inlineWidgetList = [...inlineRawWidgetMap.keys()]
