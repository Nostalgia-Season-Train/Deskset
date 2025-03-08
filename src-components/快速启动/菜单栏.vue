<script setup>
import { ref, toRaw } from 'vue'
import { desksetReq } from '../request'

const items = ref([])  // 菜单 dock 保存的元素 items

// 主题保存的菜单栏配置
const config = defineModel({ type: Object })
if (Object.keys(config.value).length != 0) {
  items.value = config.value
}

const dropFiles = async (event) => {
  const eventfiles = event.dataTransfer.files
  for (let i = 0; i < eventfiles.length; i++) {
    const dropfile = await electron.retFile(eventfiles[i])
    if (!items.value.some(i => i.path == dropfile.path)) {  // 去掉重复拖入的文件
      items.value.push(dropfile)
    }
  }
  config.value = toRaw(items.value)  // 将 Proxy 数组还原回普通数组
}

const openItem = async (item) => {
  desksetReq.get(`/v0/quick/open-default/${item.path}`)
}
</script>


<template>
<div style="height: 36px;"><!-- 撑开管理/组件预览的高度 -->
  <div class="dock"
    @drop="dropFiles"
    @drop.prevent
    @dragover.prevent
  >
    <div v-if="items.length == 0" style="color: white; font-size: 1.15em; padding: 5px;">请拖拽文件到菜单</div>
    <div class="dock-item" v-for="item in items">
      <img class="icon" :src="item.icon" @dragstart.prevent @click="openItem(item)"></img>
    </div>
  </div>
</div>
</template>


<style scoped>
* {
  --s: 1;
  --w: 36px;
  --p: 5px 10px;
}

img {
  width: 36px;
  height: 36px;
}

.dock {
  display: flex;
  justify-content: center;
  align-items: center;

  background-color: rgba(255, 255, 255, 0.25);
  border: 1px solid transparent;
  border-radius: 12px;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);

  /* 居中变化：会影响组件 auto-hide 属性 */
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;  /* 避免组件拖动后文字换行 */
}

.dock-item {
  display: flex;
  justify-content: center;
  align-items: center;

  width: var(--w);
  padding: var(--p);

  scale: var(--s);
  margin: 0 calc((var(--s) * var(--w) - var(--w)) / 2);
  transform-origin: bottom;
  transition: 0.3s ease;
}
.dock-item:hover {
  --s: 1.5
}
.dock-item:has(+ .dock-item:hover),
.dock-item:hover+ .dock-item {
  --s: 1.25;
}

/* 修复 auto-hide 自动隐藏后不显示 */
/* absolute 下 dock 不会撑开外层 div，隐藏后鼠标直接透明穿透 */
:global(#快速启动\/菜单栏>*) {
  opacity: 1;
  visibility: visible;
}
.auto-hide .dock {  /* 特殊类名加上 deskset 前缀 */
  opacity: 0.01;  /* 效果等同于 #FFFFFF01 */
  transition: opacity 0.3s ease;  /* 建议改成全局变量 */
}
.auto-hide:hover .dock {
  opacity: 1;
}
</style>
