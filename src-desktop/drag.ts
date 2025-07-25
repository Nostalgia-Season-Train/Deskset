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
        x: left + (width >> 1), y: top + (height >> 1),
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
