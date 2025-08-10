<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { exit } from '@tauri-apps/plugin-process'

import win from '#manager/global/win/manager'
import { config } from '#manager/global'

const clickCloseButton = async () => {
  if (config.closeBehavior == 'hide') {
    await win.hide()
  } else {
    await exit(0)
  }
}
</script>


<template>
<div class="container">

  <div class="left">
    <span>Deskset</span>
  </div>

  <div class="right">
    <span><Icon icon="lucide:messages-square"/></span>
    <span @click="win.minimize()"><Icon icon="lucide:minus" style="width: 18px; height: 18px;"/></span>
    <span><Icon icon="lucide:square" style="width: 14px; height: 14px;"/></span>
    <span @click="clickCloseButton" style="--hover-color: #D32F2FD0;"><Icon icon="lucide:x"/></span>
  </div>

</div>
</template>


<style lang="less" scoped>
.container {
  --hover-color: #0001;

  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;

  color: #000C;

  .left {
    height: 100%;
    display: flex;
    align-items: center;

    span {
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;

      margin-left: 7px;
      font-family: 'Rany';
      font-size: 18px;
    }
  }
  .right {
    height: 100%;
    display: flex;
    align-items: center;

    span {
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;

      width: 40px;

      transition: .3s;
      &:hover { background-color: var(--hover-color); }
    }
  }
}
</style>
