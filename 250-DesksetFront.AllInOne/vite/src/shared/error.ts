/* ==== 桌设（标准）错误 DesksetError ==== */
export class DesksetError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'DesksetError'
  }
}


/* ==== RPC 模块错误 ==== */
export class RPCIDAllocateError extends DesksetError {
  constructor() { super('Cannot allocate RPC ID') }
}


/* ==== Widget 模块错误 ==== */
export class WidgetclsNotExistError extends DesksetError {
  constructor(path: string, beInline: boolean) {
    super(`Widgetcls(path=${path}, beInline=${beInline}) not exist`)
  }
}
