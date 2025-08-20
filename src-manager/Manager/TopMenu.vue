<script lang="ts" setup>
import { Minus, Square, X } from 'lucide-vue-next'
import win from '#manager/global/win/manager'

const clickCloseButton = async () => {
  await win.close()
}
</script>


<template>
<div class="container">

  <div class="left">
    <span>Deskset</span>
  </div>

  <div class="right">
    <span @click="win.minimize()"><Minus style="width: 18px; height: 18px;"/></span>
    <span><Square style="width: 14px; height: 14px;"/></span>
    <span @click="clickCloseButton" style="--hover-color: #D32F2FD0;"><X style="width: 18px; height: 18px;"/></span>
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
