<script lang="ts" setup>
import { _t } from '#manager/main/i18n'

import { Router } from 'vue-router'
const props = defineProps<{ router: Router }>()

import { Info, Home, LayoutDashboard, Image, Palette } from 'lucide-vue-next'
import CogLoop from '#desksetui/icons/MaterialLineIcons/CogLoop.vue'
const items = [
  { icon: Info,            page: 'welcome' },
  { icon: Home,            page: 'homepage' },
  { icon: LayoutDashboard, page: 'widget' },
  { icon: Image,           page: 'wallpaper' },
  { icon: Palette,         page: 'theme' },
  { icon: CogLoop,         page: 'setting' }
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
    <span class="text">{{ _t(item.page) }}</span>
  </div>

</div>
</template>


<style lang="less" scoped>
.aside {
  width: 100%;
  height: 100%;
  background: var(--bg);

  display: flex;
  flex-direction: column;

  .logo {
    margin: 6px 8px;
    padding: 0px 4px;  // LOGO与图标左右中心对齐 (4)+28/2=(6)+24/2
    display: flex;
    align-items: center;

    -webkit-app-region: drag;

    img {
      width: 28px;
      height: 28px;
      border: solid 0 transparent;
      border-radius: 3px;
      box-shadow: var(--shadow-s)
    }
    .text {
      margin-left: 4px;  // 文字左边对齐 4+28+(4)=6+24+(6)
      font-family: 'Rany';
      font-size: 20px;
    }
  }

  .item {
    position: relative;
    margin: 3px 8px;
    padding: 3px 6px;
    display: flex;
    align-items: center;

    color: var(--text-sharp);

    transition: .3s;

    .icon {
      width: 24px;
      height: 24px;
      stroke-width: 1.6px;
    }
    .text {
      margin-left: 6px;
      font-family: 'MiSansVF';
      font-size: 20px;
      font-weight: 350;
    }
  }
  .item:hover {
    box-shadow: var(--shadow-s);
  }
  .item:active {
    background: var(--bg-light);
    box-shadow: var(--shadow-m);
  }
  .item.currentPage {
    // 色卡来源：https://www.bilibili.com/video/BV1JPJhzSEED?t=22.0
    color: #315BB8;
    background: #D0ECF4;
  }
  .item:last-child {
    margin-top: auto;
    margin-bottom: 6px;
  }
  /* --- 主页和部件间的分割线 --- */
  .item:nth-child(3) {
    margin-bottom: 6px;
  }
  .item:nth-child(4) {
    margin-top: 6px;
  }
  .item:nth-child(3)::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -7px;
    width: 100%;
    height: 2px;
    background: var(--text-sharp);
  }
}
</style>
