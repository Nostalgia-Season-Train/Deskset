<script lang="ts" setup>
import { Router } from 'vue-router'
const props = defineProps<{ router: Router }>()

import { Home, LayoutDashboard, Image, Palette, Settings } from 'lucide-vue-next'
const items = [
  { icon: Home,            text: '主页', page: 'welcome' },
  { icon: LayoutDashboard, text: '部件', page: 'widget' },
  { icon: Image,           text: '壁纸', page: 'wallpaper' },
  { icon: Palette,         text: '主题', page: 'theme' },
  { icon: Settings,        text: '设置', page: 'setting' }
]
</script>


<template>
<div class="aside">

  <div class="logo">
    <img src="/static/icons/Deskset LOGO v2.1.png" draggable="false"/>
    <span class="text">Deskset</span>
  </div>

  <div
    :class="`item ${ item.page == router.currentRoute.value.name ? 'currentPage' : '' }`"
    v-for="item in items"
    @click="$emit('jump', item.page)"
  >
    <component class="icon" :is="item.icon"/>
    <span class="text">{{ item.text }}</span>
  </div>

</div>
</template>


<style lang="less" scoped>
.aside {
  width: 100%;
  height: 100%;
  padding: 20px 16px;
  background: var(--bg);

  display: flex;
  flex-direction: column;

  .logo {
    display: flex;
    align-items: center;

    img {
      width: 48px;
      border: solid 0 transparent;
      border-radius: 3px;
      box-shadow: var(--shadow-s)
    }
    .text {
      margin-left: 10px;
      font-family: 'Rany';
      font-size: 28px;
    }
  }

  .item {
    margin-top: 20px;
    padding: 4px 8px;

    display: flex;
    align-items: center;

    color: var(--text-title);

    transition: .3s;

    .icon {
      width: 24px;
      height: 24px;
      stroke-width: 1.5px;
    }
    .text {
      margin-left: 6px;
      font-size: 20px;
    }
  }
  .item:hover {
    box-shadow: var(--shadow-s);
  }
  .item.currentPage {
    background: var(--bg-light);
    box-shadow: var(--shadow-m);
  }
  .item:last-child {
    margin-top: auto;
  }
}
</style>
