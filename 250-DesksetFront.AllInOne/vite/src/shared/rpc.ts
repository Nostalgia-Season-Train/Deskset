/* ==== RPC客户端 RPCClient ==== */
export class RPCClient {
  channel: BroadcastChannel
  waiting: Map<string, Function>

  constructor(channel: BroadcastChannel) {
    this.channel = channel
    this.channel.onmessage = this.onReceive
    this.waiting = new Map()
  }

  private hook = (funcName: string, funcArgs: any[]): Promise<any | unknown> => {
    // 生成唯一 ID
    const id = Math.random().toString(16).slice(2)

    return new Promise((resolve, reject) => {
      // 注册 ID 及回调函数
      this.waiting.set(id, (error: Error, result: any) => {
        if (error) {
          const err = new Error()
          err.name = error.name
          err.message = error.message
          err.stack = error?.stack
          reject(err)
        } else {
          resolve(result)
        }
      })

      // 发送请求
      this.channel.postMessage(
        JSON.stringify({
          id,
          funcName: funcName,
          funcArgs: [...funcArgs]
        })
      )
    })
  }

  private onReceive = async (msg: MessageEvent) => {
    const response = JSON.parse(msg.data)

    // 查找对应 ID，移除 ID 后触发回调
    const callback = this.waiting.get(response.id) as Function
    this.waiting.delete(response.id)
    callback(response.error, response.result)
  }

  helloworld = () => {
    return this.hook('helloworld', [])
  }
}


/* ==== RPC服务端 RPCServer ==== */
export class RPCServer {
  channel: BroadcastChannel

  constructor(channel: BroadcastChannel) {
    this.channel = channel
    this.channel.onmessage = this.onReceive
  }

  private onReceive = async (msg: MessageEvent) => {
    const request = JSON.parse(msg.data)

    let result, error
    try {
      result = await (this as any)[request.funcName](...request.funcArgs)
    } catch (err) {
      if (err instanceof Error) {
        error = {
          name: err.name,
          message: err.message,
          stack: err?.stack
        }
      } else {
        error = {
          name: 'unknown error',
          message: 'unknown error type',
          stack: undefined
        }
      }
    }

    this.channel.postMessage(
      JSON.stringify({
        id: request.id,
        result: result,
        error: error
      })
    )
  }

  helloworld = async () => {
    return 'helloworld'
  }
}
