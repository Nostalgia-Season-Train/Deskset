<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import win from '#manager/global/win/manager'

import { Router } from 'vue-router'
const props = defineProps<{ router: Router }>()

import { Minus, Square, X } from 'lucide-vue-next'
</script>


<template>
<div class="header">

  <div class="page">{{ _t(String(router.currentRoute.value.name ?? '')) }}</div>

  <div class="item" @click="win.minimize">
    <Minus style="width: 24px; height: 24px;"/>
  </div>
  <div class="item">
    <Square style="width: 18px; height: 18px;"/>
  </div>
  <div class="item" @click="win.close">
    <X style="width: 22px; height: 22px;"/>
  </div>

</div>
</template>


<style lang="less" scoped>
.header {
  width: 100%;
  height: 100%;
  display: flex;

  -webkit-app-region: drag;

  .page {
    margin-left: 6px;
    height: 100%;
    display: flex;
    align-items: center;

    font-family: 'MiSansVF';
    font-size: 20px;
    font-weight: 350;
  }

  .item {
    width: var(--header-height);
    height: 100%;

    display: flex;
    justify-content: center;
    align-items: center;

    transition: .3s;

    -webkit-app-region: no-drag;  /* 重置 drag 行为（normal 无法重置） */
  }
  .item:hover {
    box-shadow: var(--shadow-s);
  }
  .item:active {
    background: var(--bg);
    box-shadow: var(--shadow-m);
  }
  .item:last-child:hover {
    color: var(--bg-dark);
    background: #E81123;
  }
  .item:last-child:active {
    color: var(--bg-dark);  // 保证按住移开不变色
    background: #F1707A;
  }
  .item:nth-child(2) {
    margin-left: auto;
  }
}
</style>
