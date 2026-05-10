/* ==== 想要注册的内联部件 ==== */
const widgetclsPathList = [
  /* --- 时间和日期 --- */
  'datetime/clock'
]


/* ==== 内联部件 ==== */
import { Widgetcls } from '@src/feature/widget'

// 附：** 搜索嵌套目录（包括当前目录），* 搜索一级子目录
const widgetclsCodeMap = import.meta.glob('./*/*.vue', { import: 'default' })
const widgetclsInfoMap = import.meta.glob('./*/*.json', { import: 'default' })

let _inlineWidgetclsMap: Map<string, Widgetcls> = new Map()
for (const widgetclsPath of widgetclsPathList) {
  // 1、获取部件代码和部件信息
  const code = widgetclsCodeMap[`./${widgetclsPath}.vue`]
  if (code === undefined)
    throw Error(`Widget code ${widgetclsPath}.vue not exist`)
  const info = widgetclsInfoMap[`./${widgetclsPath}.json`]
  if (info === undefined)
    throw Error(`Widget info ${widgetclsPath}.json not exist`)
  // 2、添加部件类
  _inlineWidgetclsMap.set(widgetclsPath, {
    path: widgetclsPath,
    beInline: true,
    // @ts-ignore
    main: (await code()).render,
    // @ts-ignore
    ...(await info())
  })
}
export const inlineWidgetclsMap = _inlineWidgetclsMap
