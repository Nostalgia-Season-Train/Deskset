<script lang="ts" setup>
/* ==== 组件作用域 ==== */
  // 要让 style scoped 下的样式，在动态创建的 element 上生效
   // 需要 element 附着组件作用域 data 属性 data-v-XXXX
let dataVue: string = ''

const getDataVueAttribute = (element: Element) => {
  for (const attribute of element.getAttributeNames())
    if (attribute.startsWith('data-v'))
      return attribute
}


/* ==== 粒子生成 ==== */
import { useTemplateRef, onMounted } from 'vue'

const particleContainer = useTemplateRef('particle-container')

onMounted(async () => {
  if (particleContainer.value != null)
    dataVue = getDataVueAttribute(particleContainer.value) ?? dataVue  // ?? = get ? get : dataVue
})

const createParticle = async (event: MouseEvent) => {
  // 过滤子元素事件（会影响 offsetX 和 offsetY）
  if (event.target != particleContainer.value)
    return

  // 动态添加 html 第一步：创建 element 对象
  const particle = document.createElement('div')
  particle.setAttribute(dataVue, '')
  particle.classList.add('particle')

  // 起始位置
  particle.style.left = `${event.offsetX}px`
  particle.style.top  = `${event.offsetY}px`

  // 随机移动
  const moveX = (Math.random() - 0.5) * 400
  const moveY = (Math.random() - 0.5) * 400
  particle.style.setProperty('--move-x', `${moveX}px`)
  particle.style.setProperty('--move-y', `${moveY}px`)

  // 随机大小
  const size = Math.random() * 2 + 1
  particle.style.width  = `${size}px`
  particle.style.height = `${size}px`

  // 随机存在时间
  const duration = Math.random() * 3 + 2
  particle.style.animationDuration = `${duration}s`

  // 动态添加 html 第二步：append 插入现有节点作为其子节点
  particleContainer.value?.append(particle)
  setTimeout(async () => particle.remove(), duration * 1000)
}
</script>


<template>
<div class="container"><!-- 子组件的根节点 data-v 包含父组件 data-v -->
  <!-- 这样只有子组件自身的 data-v -->
  <div class="particle-container" ref="particle-container" @mousemove="createParticle"></div>
</div>
</template>


<style lang="less" scoped>
.container {
  width: 100%;
  height: 100%;

  .particle-container {
    width: 100%;
    height: 100%;
  }
}

.particle {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;

  // 颜色配置
  background: #FFF;
  box-shadow: inset 0 0 2px #121212,  // 圆上的细边框
              0 0 5px #BA68C8,   // 发光 1
              0 0 10px #BA68C8;  // 发光 2

  animation: animate linear forwards;
  @keyframes animate {
    0% {
      opacity: 1;
      transform: translate(0, 0), scale(1);
    }
    100% {
      opacity: 0;
      transform: translate(var(--move-x), var(--move-y)) scale(0.5);
    }
  }
}
</style>
