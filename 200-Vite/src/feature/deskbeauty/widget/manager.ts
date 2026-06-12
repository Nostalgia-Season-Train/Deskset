import { h, render } from 'vue'
import { WidgetclsNotExistError } from '@src/shared/error'
import { RPCClient, RPCServer } from '@src/shared/rpc'
import { Widgetcls } from './type'


export abstract class AbstractWidgetManager {
  // 添加部件
  abstract appendWidget(path: string, beInline: boolean): Promise<void>
}


export class WidgetManagerClient
  extends RPCClient
  implements AbstractWidgetManager
{
  constructor(channel: BroadcastChannel) {
    super(channel)
  }

  async appendWidget(path: string, beInline: boolean) {
    // 这里可以反射原型链，生成 hook 调用，但为了行为可控手动编写
    return await this.hook('appendWidget', [path, beInline])
  }
}


export class WidgetManagerServer
  extends RPCServer
  implements AbstractWidgetManager
{
  private _inlineWidgetclsMap: Map<string, Widgetcls>
  private _el: HTMLElement

  constructor(
    channel: BroadcastChannel,
    inlineWidgetclsMap: Map<string, Widgetcls>,
    el: HTMLElement
  ) {
    super(channel)
    this._inlineWidgetclsMap = inlineWidgetclsMap
    this._el = el
  }

  async appendWidget(path: string, beInline: boolean) {
    // 取出 widgetcls 部件类
    let widgetcls: Widgetcls | undefined
    if (beInline) {
      widgetcls = this._inlineWidgetclsMap.get(path)
    }
    if (widgetcls === undefined)
      throw new WidgetclsNotExistError(path, beInline)

    const main = widgetcls.main
    const vnode = h({ render: main })
    render(vnode, this._el)
    return
  }
}
