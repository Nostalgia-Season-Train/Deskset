<script lang="ts" setup>
import { Icon } from '@iconify/vue'

import win from '#manager/global/win/manager'
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
    <span @click="win.hide()" style="--hover-color: #D32F2FD0;"><Icon icon="lucide:x"/></span>
  </div>

</div>
</template>


<style lang="less" scoped>
.container {
  --hover-color: #FFF1;

  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;

  color: white;

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

      transition: .5s;
      &:hover { background-color: var(--hover-color); }
    }
  }
}
</style>
