import { h, render } from 'vue'
import { RPCClient, RPCServer } from '@src/shared/rpc'
import { Widgetcls } from './type'


export abstract class AbstractWidgetManager {
  abstract helloworld(): Promise<string>
  // 添加部件
  abstract appendWidget(path: string): Promise<void>
}


// @ts-expect-error: client 的 RPC 方法由 createProxyMethods 生成
export class WidgetManagerClient extends AbstractWidgetManager {
  private _rpcClient: RPCClient

  constructor(channel: BroadcastChannel) {
    super()
    this._rpcClient = new RPCClient(channel)
    this._createProxyMethods()
  }

  // 通过反射创建代理，绑定 RPC 方法到 this 上
  private _createProxyMethods() {
    // AbstractWidgetManager 中的方法是纯类型声明，运行时不存在
    const prototype = WidgetManagerServer.prototype
    const propertyNames = Object.getOwnPropertyNames(prototype)
    for (const name of propertyNames) {
      if (name === 'constructor')
        continue
      const descriptor = Object.getOwnPropertyDescriptor(prototype, name)
      if (descriptor === undefined || typeof descriptor.value !== 'function')
        continue
      // hook 返回 Promise，不要用异步函数
      (this as any)[name] = (...args: any[]) => {
        return this._rpcClient.hook(name, args)
      }
    }
  }
}


export class WidgetManagerServer extends AbstractWidgetManager {
  // @ts-expect-error: rpcServer 自动调用 this 方法
  private _rpcServer: RPCServer
  private _inlineWidgetclsMap: Map<string, Widgetcls>
  private _el: HTMLElement

  constructor(
    channel: BroadcastChannel,
    inlineWidgetclsMap: Map<string, Widgetcls>,
    el: HTMLElement
  ) {
    super()
    this._rpcServer = new RPCServer(channel, this)
    this._inlineWidgetclsMap = inlineWidgetclsMap
    this._el = el
  }

  async helloworld() {
    return 'helloworld'
  }

  async appendWidget(path: string) {
    // - [ ] 后面抛出错误
    if (!this._inlineWidgetclsMap.has(path))
      return
    const main = this._inlineWidgetclsMap.get(path)!.main
    const vnode = h({ render: main })
    render(vnode, this._el)
    return
  }
}
