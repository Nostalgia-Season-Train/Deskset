import { DesktopChannel } from '../channel.ts'


class BroadcastDesktopClient {
  broadcast: BroadcastChannel
  waiting: Map<string, Function>

  constructor() {
    this.broadcast = DesktopChannel
    this.broadcast.onmessage = this.onReceive
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
      this.broadcast.postMessage(
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

  appendWidget = (
    id: string,
    name: string,
    option: {
      isDragLock?: boolean | null,
      isDisableInteract?: boolean | null,
      isAutoHide?: boolean | null,
      left?: number | null,
      top?: number | null,
      scale?: number | null,
      model?: Record<string, any>
    } = {
      isDragLock: null,
      isDisableInteract: null,
      isAutoHide: null,
      left: null,
      top: null,
      scale: null,
      model: {}
    }
  ): Promise<{
    isDragLock: boolean,
    isDisableInteract: boolean,
    isAutoHide: boolean,
    x: number,
    y: number,
    left: number,
    top: number,
    scale: number,
    model: Record<string, any>
  }> => {
    return this.hook('appendWidget', [
      id,
      name,
      option.isDragLock,
      option.isDisableInteract,
      option.isAutoHide,
      option.left,
      option.top,
      option.scale,
      option.model
    ])
  }
  removeWidget = (id: string): Promise<void> => {
    return this.hook('removeWidget', [id])
  }
  editWidget = (id: string, model: Record<string, any>) => {
    return this.hook('editWidget', [id, model])  // 不返回任何值，model 通过 DesktopSend 更新
  }
  locateWidget = (id: string) => {
    return this.hook('locateWidget', [id])
  }

  setWidgetAxis = (id: string, x: number | null = null, y: number | null = null): Promise<{ x: number, y: number, left: number, top: number }> => {
    return this.hook('setWidgetAxis', [id, x, y])
  }
  setWidgetScale = (id: string, scale: number) => {
    return this.hook('setWidgetScale', [id, scale])
  }
  switchWidgetProp = (id: string, prop: string, state: boolean): Promise<void> => {
    return this.hook('switchWidgetProp', [id, prop, state])
  }

  getWindowData = (): Promise<{ width: number, height: number, dpr: number }> => {
    return this.hook('getWindowData', [])
  }

  getWindowPicture = (): Promise<number[]> => {
    return this.hook('getWindowPicture', [])
  }
}


export default new BroadcastDesktopClient()
