import { RPC_ID_ALLOCATE_MAXRETRY_TIME } from '@src/shared/constant'
import { RPCIDAllocateError } from '@src/shared/error'


/* ==== RPC客户端 RPCClient ==== */
export class RPCClient {
  private channel: BroadcastChannel
  private waiting: Map<string, Function>

  constructor(channel: BroadcastChannel) {
    this.channel = channel
    this.channel.onmessage = this.onReceive
    this.waiting = new Map()
  }

  hook = (funcName: string, funcArgs: any[]): Promise<any | unknown> => {
    // 生成唯一 ID
    let id: string
    for (let n = 0; n < RPC_ID_ALLOCATE_MAXRETRY_TIME; n++) {
      id = Math.random().toString(16).slice(2)
      if (!this.waiting.has(id)) break
    }
    if (this.waiting.has(id!)) throw new RPCIDAllocateError()  // ! 断言 id 已赋值

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
}


/* ==== RPC服务端 RPCServer ==== */
export class RPCServer {
  private channel: BroadcastChannel
  private instance: any

  constructor(channel: BroadcastChannel, instance: any) {
    this.channel = channel
    this.instance = instance
    this.channel.onmessage = this.onReceive
  }

  private onReceive = async (msg: MessageEvent) => {
    const request = JSON.parse(msg.data)

    let result, error
    try {
      result = await (this.instance)[request.funcName](...request.funcArgs)
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
}
