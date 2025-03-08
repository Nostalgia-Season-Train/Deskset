function dragAndDrop(el) {
  return function down(event) {
    // drag-lock 锁定拖动
    if (el.classList.contains('drag-lock')) {
      return
    }

    let originX = el.offsetLeft
    let originY = el.offsetTop
    let beginX = event.clientX
    let beginY = event.clientY

    const move = (event) => {
      let moveX = event.clientX - beginX
      let moveY = event.clientY - beginY

      this.style.position = "fixed"

      this.style.left = moveX + originX + "px"
      this.style.top  = moveY + originY + "px"
    }

    const up = () => {
      document.removeEventListener("mousemove", move)
      document.removeEventListener("mouseup", up)
    }

    document.addEventListener("mousemove", move)
    document.addEventListener("mouseup", up)
  }
}

/* export default 后，import 任意符号 from 文件 */
export default {
  /* 以插件形式暴露自定义指令 */
  install(app) {
    /* widgetDrag 对应 v-widget-drag 指令 */
    app.directive("widgetDrag", {
      mounted: (el, binding) => {
        binding.value = dragAndDrop(el)
        el.addEventListener("mousedown", binding.value)
      },
      unmounted: (el, binding) => {
        el.removeEventListener("mousedown", binding.value)
      }
    })
  }
}
