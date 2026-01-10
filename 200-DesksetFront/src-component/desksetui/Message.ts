import { h, render } from 'vue'

import MessageSFC from './MessageSFC.vue'

export function message(
  title: string,
  content: string,
  cancel: string = '取消',
  confirm: string = '确认'
): Promise<boolean> {
  return new Promise((resolve, reject) => {
    const vnode = h(MessageSFC, {
      title,
      content,
      cancel,
      confirm,

      onDestory: () => {
        // 组件卸载：不要在 onClose 等函数中使用，让组件执行清理逻辑后回调
        render(null, container)
        document.body.removeChild(container)
      },

      onClose: () => {
        resolve(false)
      },
      onCancel: () => {
        resolve(false)
      },
      onConfirm: () => {
        resolve(true)
      }
    })

    // 组件挂载
    const container = document.createElement('div')
    render(vnode, container)
    document.body.appendChild(container)
  })
}

import MessageInputSFC from './MessageInputSFC.vue'

export function messageInput(
  title: string,
  content: string,
  placeholder: string,
  cancel: string = '取消',
  confirm: string = '确认'
): Promise<string | null> {
  return new Promise((resolve, reject) => {
    const vnode = h(MessageInputSFC, {
      title,
      content,
      placeholder,
      cancel,
      confirm,

      onDestory: () => {
        render(null, container)
        document.body.removeChild(container)
      },

      onClose: () => {
        resolve(null)
      },
      onCancel: () => {
        resolve(null)
      },
      onConfirm: (input: string) => {
        resolve(input)
      }
    })

    const container = document.createElement('div')
    render(vnode, container)
    document.body.appendChild(container)
  })
}
