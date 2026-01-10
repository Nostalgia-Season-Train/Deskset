const dpr = window.devicePixelRatio  // 设备像素比 = Windows DPI 缩放

export default function dragAndDrop(el: HTMLElement) {
  return function down(event: MouseEvent) {
    // drag-lock 锁定拖动
    if (el.classList.contains('deskset_drag-lock')) {
      return
    }

    const id = el.id
    const broadcast = new BroadcastChannel('DesktopSend')
    const width = el.offsetWidth
    const height = el.offsetHeight

    const originX = el.offsetLeft
    const originY = el.offsetTop
    const beginX = event.clientX
    const beginY = event.clientY

    const move = (event: MouseEvent) => {
      const left = event.clientX - beginX + originX
      const top  = event.clientY - beginY + originY

      el.style.position = 'absolute'
      el.style.left = left + 'px'
      el.style.top  = top  + 'px'

      broadcast.postMessage({
        id: id,
        // 乘以 dpr 得到中心点在屏幕上的实际位置（物理像素位置）
        // 位运算：除二 >> 1；取整 | 0（仅适用于 32 位数）
        // 注：计算 container 中心点，内部元素溢出会使视觉中心点与结果不一致
        x: (left + (width >> 1)) * dpr | 0, y: (top + (height >> 1)) * dpr | 0,
        left: left, top: top
      })
    }

    const up = () => {
      document.removeEventListener('mousemove', move)
      document.removeEventListener('mouseup', up)
    }

    document.addEventListener('mousemove', move)
    document.addEventListener('mouseup', up)
  }
}
