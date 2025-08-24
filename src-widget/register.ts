export const prefixMark = '/@Deskset/'

export const inlineRawWidgetMap = new Map([
  [`${prefixMark}DigitalClock`, {
    // @ts-ignore
    main: () => import('/src-widget/时间日期/简单时间：24时.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '以 HHmm 格式，显示现在时间'
    }
  }],
  [`${prefixMark}FlipClock`, {
    // @ts-ignore
    main: () => import('/src-widget/简约系列/翻页时钟.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '以 HHmmss 格式，显示现在时间'
    }
  }],
  [`${prefixMark}Stopwatch`, {
    // @ts-ignore
    main: () => import('/src-widget/简约系列/计时器.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '测量时间经过',
      model: {
        lowcolor: '#4FC3F7'
      },
      options: [{
        name: '低位颜色',
        type: 'ColorPicker'
      }]
    }
  }],
  [`${prefixMark}Greeting`, {
    // @ts-ignore
    main: () => import('/src-widget/问候语/打字机问候.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '根据当前时段，显示个性化问候语'
    }
  }],
  [`${prefixMark}圆环监控`, {
    // @ts-ignore
    main: () => import('/src-widget/系统监控/圆环监控.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '查看芯片和内存的占用率'
    }
  }],
])

export const inlineWidgetList = [...inlineRawWidgetMap.keys()]
