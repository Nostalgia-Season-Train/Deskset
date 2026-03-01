<script lang="ts" setup>
import { _t } from '#manager/main/i18n'

import { Router } from 'vue-router'
const props = defineProps<{ router: Router }>()

import { PanelLeft, Sparkles } from 'lucide-vue-next'
import { Info, Home, Dashboard, Image, Palette } from '#desksetui/icons/Google Material Icons'
import CogLoop from '#desksetui/icons/Material Line Icons/CogLoop.vue'
const items = [
  { icon: Info,      page: 'welcome' },
  // { icon: Home,      page: 'homepage' },
  { icon: Dashboard, page: 'widget' },
  // { icon: Image,     page: 'wallpaper' },
  { icon: Palette,   page: 'theme' },
  { icon: Sparkles,  page: 'ai' },
  { icon: CogLoop,   page: 'setting' }
]
</script>


<template>
<div class="aside">

  <div class="logo">
    <div class="logo__content">
      <img src="/static/icons/Deskset LOGO v2.1.png" draggable="false"/>
      <span class="text">Deskset</span>
      <PanelLeft/><!-- 控制侧边栏折叠，目前仅起装饰作用 -->
    </div>
  </div>

  <div
    class="item"
    v-for="item in items"
    @click="$emit('jump', item.page)"
  >
    <div :class="`item__content ${ item.page == router.currentRoute.value.name ? 'currentPage' : '' }`">
      <component class="icon" :is="item.icon"/>
      <span class="text">{{ _t(item.page) }}</span>
    </div>
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
    position: relative;
    padding: 6px 8px;
    -webkit-app-region: drag;
    .logo__content {
      display: flex;
      align-items: center;
      img {
        width: 28px;
        height: 28px;
        border: solid 0 transparent;
        border-radius: 3px;
        box-shadow: var(--shadow-s)
      }
      .text {
        margin-left: 4px;
        font-family: 'Rany';
        font-size: 20px;
      }
      &>:last-child {
        margin-left: auto;
      }
    }
  }

  .item {
    position: relative;
    padding: 4px 6px;
    .item__content {
      padding: 2px 4px;
      display: flex;
      align-items: center;
      color: var(--deskset-text-sharp-color);
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
  }
  .item__content:hover {
    box-shadow: var(--shadow-s);
  }
  .item__content:active {
    background: var(--bg-light);
    box-shadow: var(--shadow-m);
  }
  .item__content.currentPage {
    // 色卡来源：https://www.bilibili.com/video/BV1JPJhzSEED?t=22.0
    color: var(--deskset-color-primary);
    background: var(--deskset-color-primary-light-9);
  }
  .item:last-child {
    margin-top: auto;
  }
  /* --- 分割线 --- */
  // .item:nth-child(3)::after {
  //   content: '';
  //   position: absolute;
  //   left: 0;
  //   bottom: 0;
  //   width: 100%;
  //   height: 1px;
  //   opacity: .5;
  //   background: var(--deskset-text-sharp-color);
  // }
}
</style>
