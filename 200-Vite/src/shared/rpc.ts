import {
  RPC_ID_ALLOCATE_MAXRETRY_TIME,
  RPC_TIMEOUT_MILLISECOND_NUM
} from '@src/shared/constant'
import {
  RPCIDAllocateError,
  RPCTimeoutError
} from '@src/shared/error'


/* ==== RPC客户端 RPCClient ==== */
export class RPCClient {
  private _channel: BroadcastChannel
  private _waiting: Map<string, Function>

  constructor(channel: BroadcastChannel) {
    this._channel = channel
    this._channel.onmessage = this._onReceive
    this._waiting = new Map()
  }

  hook = (funcName: string, funcArgs: any[]): Promise<any | unknown> => {
    // 生成唯一 ID
    let id: string
    for (let n = 0; n < RPC_ID_ALLOCATE_MAXRETRY_TIME; n++) {
      id = Math.random().toString(16).slice(2)
      if (!this._waiting.has(id)) break
    }
    if (this._waiting.has(id!)) throw new RPCIDAllocateError()  // ! 断言 id 已赋值

    return new Promise((resolve, reject) => {
      // 设置超时
      const timeout = setTimeout(() => {
        this._waiting.delete(id)
        reject(new RPCTimeoutError(id, funcName))
      }, RPC_TIMEOUT_MILLISECOND_NUM)
      // 注册 ID 及回调函数
      this._waiting.set(id, (error?: Error, result?: any) => {
        // 1、清除超时
        clearTimeout(timeout)
        // 2、返回错误或结果
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
      this._channel.postMessage({
        id,
        funcName: funcName,
        funcArgs: [...funcArgs]
      })
    })
  }

  private _onReceive = async (msg: MessageEvent) => {
    const response = msg.data

    // 查找对应 ID，移除 ID 后触发回调
    const callback = this._waiting.get(response.id) as Function
    this._waiting.delete(response.id)
    callback(response.error, response.result)
  }
}


/* ==== RPC服务端 RPCServer ==== */
export class RPCServer {
  private _channel: BroadcastChannel

  constructor(channel: BroadcastChannel) {
    this._channel = channel
    this._channel.onmessage = this._onReceive
  }

  private _onReceive = async (msg: MessageEvent) => {
    const request = msg.data

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

    this._channel.postMessage({
      id: request.id,
      result: result,
      error: error
    })
  }
}
