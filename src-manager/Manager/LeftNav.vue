<script lang="ts" setup>
import { ref, defineEmits } from 'vue'
import { Icon } from '@iconify/vue'

const emit = defineEmits(['jump'])  // 此 emit 非 $emit


/* === 侧边栏 === */
const upItems = [
  { type: 'option', icon: 'line-md:chat-round', text: '欢迎', page: 'welcome' },
  { type: 'option', icon: 'line-md:home',       text: '主页', page: 'homepage' },
  { type: 'line' },  // 暂时没有 icon 和 text 居中的分割线样式
  { type: 'option', icon: 'line-md:grid-3-filled', text: '浮动', page: 'float' },
  { type: 'option', icon: 'line-md:list-3-filled', text: '组件', page: 'widget' },
  { type: 'option', icon: 'line-md:image-filled',  text: '主题', page: 'theme' }
]
const downItems = [
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
  <div @mousemove="setLightPos" class="nav">

    <div class="up menu">
      <!-- 注 1：href 用于 a 标签，对 div 无影响 -->
      <component
        v-for="item in upItems"
        :is="item.type == 'option' ? 'a' : 'div'"
        :class="`item ${item.type}`"
        @click="select(item?.page)"
        href="#"
      >
        <div class="icon" v-if="item?.icon"><Icon :icon="item.icon"/></div>
        <div class="text" v-if="item?.text"><span>{{ item.text }}</span></div>
      </component>
    </div>

    <div class="down menu">
      <component
        v-for="item in downItems"
        :is="item.type == 'option' ? 'a' : 'div'"
        :class="`item ${item.type}`"
        @click="select(item?.page)"
        href="#"
      >
        <div class="icon" v-if="item?.icon"><Icon :icon="item.icon"/></div>
        <div class="text" v-if="item?.text"><span>{{ item.text }}</span></div>
      </component>
    </div>

  </div>
</div>
</template>


<style lang="less" scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.nav {
  --fold-width: 60px;     // 折叠宽度
  --expand-width: 210px;  // 展开宽度

  --item-gap: 5px;   // 元素之间间隔（上下间距）
  --item-side: 5px;  // 元素跟边缘间间隔（左右间距）
  --item-height: 35px;  // 元素高度
  --item-color: black;  // 元素颜色

  --line-width: 1px;  // 描边宽度

  position: fixed;
  top: 0;
  left: 0;

  width: var(--fold-width);
  height: 100vh;
  padding: var(--line-width);

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  overflow: hidden;
  white-space: nowrap;

  .item {
    margin: var(--item-gap) var(--item-side);
    height: var(--item-height);

    display: flex;
    align-items: center;

    text-decoration: none;

    color: var(--item-color);

    .icon {
      min-width: calc(var(--fold-width) - 2 * var(--item-side) - 2 * var(--line-width));
      min-height: 100%;

      display: flex;
      justify-content: center;
      align-items: center;

      font-size: 20px;
    }
    span {
      opacity: 0;
      font-size: 16px;
    }
  }
  .line {
    height: 2px;
    background: content-box var(--item-color);
  }
}

/* --- 动画 --- */
.nav {
  transition: ease .5s;
  .item {
    transition: ease .5s;
    svg { transition: ease .5s; }
    span { transition: ease .5s; }
  }

  &:hover {
    width: var(--expand-width);
    span { opacity: 1; }
  }

  .item.option:hover {
    color: white;
    background-color: #FFF1;
  }
}
</style>

<!-- 流光 -->
<!-- 注 1：less 跟 v-bind 冲突 -->
<style scoped>
.nav {
  --light-color: white;
}

/* --- 流光：光源 --- */
.nav::before {
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
.nav::after {
  content: '';
  position: absolute;
  z-index: -1;  /* 滤镜在图标文字之下 */

  background-color: #333;
  inset: var(--line-width);
  right: calc(var(--line-width) - 0.3px);  /* 窗口边缘处的光线（上下左）会比窗口内部少些宽度，窗内减去 0.3px 平衡视觉效果 */
}

.nav:hover::before {
  opacity: 1;
}
</style>
