export default function dragAndDrop(el: HTMLElement) {
  return function down(event: MouseEvent) {
    // drag-lock 锁定拖动
    if (el.classList.contains('deskset_drag-lock')) {
      return
    }

    const originX = el.offsetLeft
    const originY = el.offsetTop
    const beginX = event.clientX
    const beginY = event.clientY

    const move = (event: MouseEvent) => {
      const moveX = event.clientX - beginX
      const moveY = event.clientY - beginY

      el.style.position = 'absolute'

      el.style.left = moveX + originX + 'px'
      el.style.top  = moveY + originY + 'px'
    }

    const up = () => {
      document.removeEventListener('mousemove', move)
      document.removeEventListener('mouseup', up)
    }

    document.addEventListener('mousemove', move)
    document.addEventListener('mouseup', up)
  }
}
