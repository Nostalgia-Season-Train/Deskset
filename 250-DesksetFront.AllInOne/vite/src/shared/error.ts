/* ==== 桌设（标准）错误 DesksetError ==== */
export class DesksetError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'DesksetError'
  }
}


/* ==== RPC 错误 ==== */
export class RPCIDAllocateError extends DesksetError {
  constructor() { super('Cannot allocate RPC ID') }
}
