import dayjs from 'dayjs'

export const prefixMark = '/@Deskset/'

export const inlineRawWidgetMap = new Map([
  /* --- Note --- */
  [`${prefixMark}Base`, {
    // @ts-ignore
    main: () => import('/src-widget/note/base.vue'),
    // @ts-ignore
    metainfo: await import('/src-widget/note/base.json')
  }],

  /* --- 时间与日期 --- */
  [`${prefixMark}DigitalClock`, {
    // @ts-ignore
    main: () => import('/src-widget/时间与日期/数字时钟.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '以 HHmm 格式，显示现在时间',
      model: {
        time_color: '#FFFFFFF0',
        date_color: '#FFFFFFA0'
      },
      options: [{
        name: '时间文字颜色',
        type: 'ColorPicker',
        key: 'time_color'
      }, {
        name: '日期文字颜色',
        type: 'ColorPicker',
        key: 'date_color'
      }]
    }
  }],
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
  [`${prefixMark}Stopwatch`, {
    // @ts-ignore
    main: () => import('/src-widget/时间与日期/秒表.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '测量时间经过',
      model: {
        highcolor: '#000000C0',
        lowcolor: '#000000'
      },
      options: [{
        name: '高位颜色',
        type: 'ColorPicker',
        key: 'highcolor'
      }, {
        name: '低位颜色',
        type: 'ColorPicker',
        key: 'lowcolor'
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

  /* --- 笔记 --- */
  [`${prefixMark}VaultStats`, {
    // @ts-ignore
    main: () => import('/src-widget/笔记/仓库统计.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '统计仓库的笔记数量、附件数量和累计使用天数'
    }
  }],
  [`${prefixMark}NoteStats`, {
    // @ts-ignore
    main: () => import('/src-widget/笔记/笔记统计.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '通过条件过滤笔记后统计数量，双击随机打开其中一篇笔记',
      model: {
        // 基础
        title: '📝笔记总数',
        // 筛选
        filterGroup: {
          match: 'all',
          filters: []
        },
        // 样式
        width: 200,
        height: 100,
        titleColor: '#000000',
        numberColor: '#000000',
        backgroundColor: '#FFFFFF'
      },
      options: [{
        name: '基础',
        type: 'tab',
        content: [{
          name: '标题（可以插入 Emoji 表情）',
          type: 'Input',
          key: 'title'
        }]
      }, {
        name: '筛选',
        type: 'tab',
        content: [{
          name: '点击右边的按钮，加入一个条件',
          type: 'ArrayFilter',
          key: 'filterGroup'
        }]
      }, {
        name: '样式',
        type: 'tab',
        content: [{
          name: '宽度',
          type: 'InputNumber',
          key: 'width'
        }, {
          name: '高度',
          type: 'InputNumber',
          key: 'height'
        }, {
          name: '标题颜色',
          type: 'ColorPicker',
          key: 'titleColor'
        }, {
          name: '数字颜色',
          type: 'ColorPicker',
          key: 'numberColor'
        }, {
          name: '背景颜色',
          type: 'ColorPicker',
          key: 'backgroundColor'
        }]
      }]
    }
  }],
  [`${prefixMark}Diary`, {
    // @ts-ignore
    main: () => import('/src-widget/笔记/日记.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '展示今天的日记，双击在 Obsidian 中打开'
    }
  }],
  [`${prefixMark}待办日历`, {
    // @ts-ignore
    main: () => import('/src-widget/笔记/待办日历.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '在事件日历里统计日记中的待办事项'
    }
  }],
])

export const inlineWidgetList = [...inlineRawWidgetMap.keys()]
