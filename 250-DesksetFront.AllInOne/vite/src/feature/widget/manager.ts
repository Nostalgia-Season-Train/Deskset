import { RPCClient, RPCServer } from '@src/shared/rpc'


export abstract class AbstractWidgetManager {
  abstract helloworld(): Promise<string>
}


// @ts-expect-error: client 的 RPC 方法由 createProxyMethods 生成
export class WidgetManagerClient extends AbstractWidgetManager {
  private rpcClient: RPCClient

  constructor(channel: BroadcastChannel) {
    super()
    this.rpcClient = new RPCClient(channel)
    this.createProxyMethods()
  }

  // 通过反射创建代理，绑定 RPC 方法到 this 上
  private createProxyMethods() {
    // AbstractWidgetManager 中的方法是纯类型声明，运行时不存在
    const prototype = WidgetManagerServer.prototype
    const propertyNames = Object.getOwnPropertyNames(prototype)
    for (const name of propertyNames) {
      if (name === 'constructor')
        continue
      const descriptor = Object.getOwnPropertyDescriptor(prototype, name)
      if (descriptor === undefined || typeof descriptor.value !== 'function')
        continue
      (this as any)[name] = async (...args: any[]) => {
        return this.rpcClient.hook(name, args)
      }
    }
  }
}


export class WidgetManagerServer extends AbstractWidgetManager {
  // @ts-expect-error: rpcServer 自动调用 this 方法
  private rpcServer: RPCServer

  constructor(channel: BroadcastChannel) {
    super()
    this.rpcServer = new RPCServer(channel, this)
  }

  async helloworld() {
    return 'helloworld'
  }
}
