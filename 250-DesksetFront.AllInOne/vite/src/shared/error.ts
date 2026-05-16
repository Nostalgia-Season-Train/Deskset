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
export class RPCTimeoutError extends DesksetError {
  constructor(callName: string) {
    super(`RPC call '${callName}' timeout`)
  }
}


/* ==== Widget 模块错误 ==== */
export class WidgetclsNotExistError extends DesksetError {
  constructor(path: string, beInline: boolean) {
    super(`Widgetcls(path=${path}, beInline=${beInline}) not exist`)
  }
}
export class WidgetIDAllocateError extends DesksetError {
  constructor() { super('Cannot allocate Widget ID') }
}
