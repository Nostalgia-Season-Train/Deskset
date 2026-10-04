/* ==== 桌设（标准）错误 DesksetError ==== */
export class DesksetError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'DesksetError'
  }
}
