export interface Cache {
  mtime: string | null  // null 代表 mtime 获取失败
  jsModule: string  // js 模块 url 地址
  cssCode: string   // css 代码
}

export const compileCache = new Map<string, Cache>()
