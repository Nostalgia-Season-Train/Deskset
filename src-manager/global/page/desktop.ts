class BroadcastDesktopClient {
  broadcast: BroadcastChannel
  waiting: Map<string, Function>

  constructor() {
    this.broadcast = new BroadcastChannel('Desktop')
    this.broadcast.onmessage = this.onReceive
    this.waiting = new Map()
  }

  private hook = (funcName: string, funcArgs: any[]): Promise<any | unknown> => {
    // 生成唯一 ID
    const id = Math.random().toString(16).slice(2)

    return new Promise((resolve, reject) => {
      // 注册 ID 及回调函数
      this.waiting.set(id, (error: unknown, result: any) => {
        if (error)
          reject(error)
        else
          resolve(result)
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

  appendWidget = (id: string, name: string): Promise<{ x: number, y: number, left: number, top: number }> => {
    return this.hook('appendWidget', [id, name])
  }

  removeWidget = (id: string): Promise<void> => {
    return this.hook('removeWidget', [id])
  }

  switchWidgetProp = (id: string, prop: string, state: boolean): Promise<void> => {
    return this.hook('switchWidgetProp', [id, prop, state])
  }

  setWidgetPosition = (id: string, left: number, top: number) => {
    return this.hook('setWidgetPosition', [id, left, top])
  }
}


export default new BroadcastDesktopClient()
