export const prefixMark = '/@Deskset/'

export const inlineRawWidgetMap = new Map([
  [`${prefixMark}数字时钟`, {
    // @ts-ignore
    main: () => import('/src-widget/时间日期/简单时间：24时.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '以 HHmm 格式，显示现在时间'
    }
  }],
  [`${prefixMark}翻页时钟`, {
    // @ts-ignore
    main: () => import('/src-widget/简约系列/翻页时钟.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '以 HHmmss 格式，显示现在时间'
    }
  }],
  [`${prefixMark}秒表`, {
    // @ts-ignore
    main: () => import('/src-widget/简约系列/计时器.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '测量时间经过'
    }
  }],
  [`${prefixMark}问候语`, {
    // @ts-ignore
    main: () => import('/src-widget/问候语/打字机问候.vue'),
    metainfo: {
      author: '旧日丨四季列车',
      version: 'v0.0.1',
      descript: '根据当前时段，显示个性化问候语'
    }
  }],
])

export const inlineWidgetList = [...inlineRawWidgetMap.keys()]
