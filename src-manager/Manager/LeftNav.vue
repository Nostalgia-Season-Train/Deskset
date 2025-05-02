<script lang="ts" setup>
import { ref, defineEmits } from 'vue'
import { Icon } from '@iconify/vue'

const emit = defineEmits(['jump'])  // 此 emit 非 $emit


/* === 侧边栏 === */
const upBoxs = [
  { type: 'option', icon: 'line-md:chat-round', text: '欢迎', page: 'welcome' },
  { type: 'option', icon: 'line-md:home',       text: '主页', page: 'homepage' },
  { type: 'split' },  // 暂时没有 icon 和 text 居中的分割线样式
  { type: 'option', icon: 'line-md:grid-3-filled', text: '浮动', page: 'float' },
  { type: 'option', icon: 'line-md:list-3-filled', text: '组件', page: 'widget' },
  { type: 'option', icon: 'line-md:image-filled',  text: '主题', page: 'theme' }
]
const downBoxs = [
  { type: 'option', icon: 'line-md:cog-loop', text: '设置', page: 'setting' }
]

const select = async (page: string | undefined) => {
  if (page != undefined)
    emit('jump', page)
}


/* === 流光 === */
const lightAxisX = ref(0)
const lightAxisY = ref(0)

const setLightPos = async (e: MouseEvent) => {
  lightAxisX.value = e.clientX  // 子元素会影响 offsetX
  lightAxisY.value = e.clientY
}
</script>


<template>
<div class="container">
  <div @mousemove="setLightPos" class="shell">

    <div class="up">
      <!-- 注 1：href 用于 a 标签，对 div 无影响 -->
      <component
        v-for="box in upBoxs"
        :is="box.type == 'option' ? 'a' : 'div'"
        :class="`box ${box.type}`"
        @click="select(box?.page)"
        href="#"
      >
        <Icon v-if="box?.icon" :icon="box.icon"/>
        <span v-if="box?.text">{{ box.text }}</span>
      </component>
    </div>

    <div class="down">
      <component
        v-for="box in downBoxs"
        :is="box.type == 'option' ? 'a' : 'div'"
        :class="`box ${box.type}`"
        @click="select(box?.page)"
        href="#"
      >
        <Icon v-if="box?.icon" :icon="box.icon"/>
        <span v-if="box?.text">{{ box.text }}</span>
      </component>
    </div>

  </div>
</div>
</template>


<style lang="less" scoped>
.shell {
  --fold-width: 60px;     // 折叠宽度
  --expand-width: 210px;  // 展开宽度
  --color: black;  // 图标文字颜色
  --line-width: 1px;  // 描边宽度

  position: fixed;
  top: 0;
  left: 0;

  box-sizing: border-box;
  width: var(--fold-width);
  height: 100vh;
  padding: var(--line-width);

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  overflow: hidden;  // 溢出隐藏
  white-space: nowrap;  // 不换行

  .box {
    margin: 10px 0 10px 0;

    display: flex;
    align-items: center;

    text-decoration: none;  // 去掉 a 标签下划线

    color: var(--color);

    svg {
      width: calc(var(--fold-width) - 2 * var(--line-width));  // svg = shell 内容区宽度，这样图标正好居中
      min-width: calc(var(--fold-width) - 2 * var(--line-width));  // 消除 flex 影响
      font-size: 20px;
    }
    span {
      opacity: 0;  // 配合动画（见下）渐变显示
      font-size: 16px;
    }
  }
  .split {
    padding: 0 5px 0 5px;
    height: 2px;
    background: content-box var(--color);  // content-box 限定背景色在内容区
  }
}

/* --- 动画 --- */
.shell {
  transition: ease .5s;
  svg { transition: ease .5s; }
  span { transition: ease .5s; }

  &:hover {
    width: var(--expand-width);
    span { opacity: 1; }
  }
}
</style>

<!-- 流光 -->
<!-- 注 1：less 跟 v-bind 冲突 -->
<style scoped>
.shell {
  --light-color: white;
}

/* --- 流光：光源 --- */
.shell::before {
  content: '';
  position: absolute;
  z-index: -2;  /* 光源在滤镜之下 */

  left: v-bind(lightAxisX + 'px');
  top: v-bind(lightAxisY + 'px');
  transform: translate(-50%, -50%);

  width: 300px;
  height: 300px;
  background: radial-gradient(var(--light-color), transparent, transparent);

  opacity: 0;
  transition: .5s, top 0s, left 0s;
}
/* --- 流光：滤镜 --- */
.shell::after {
  content: '';
  position: absolute;
  z-index: -1;  /* 滤镜在图标文字之下 */

  background-color: #333;
  inset: var(--line-width);
  right: calc(var(--line-width) - 0.3px);  /* 窗口边缘处的光线（上下左）会比窗口内部少些宽度，窗内减去 0.3px 平衡视觉效果 */
}

.shell:hover::before {
  opacity: 1;
}
.shell .box:hover {
  color: var(--light-color);
}
</style>
