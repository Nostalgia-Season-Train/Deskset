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
  }]
])

export const inlineWidgetList = [...inlineRawWidgetMap.keys()]
