<script lang="ts" setup>
import desktop from '#manager/broadcast/desktop'

const refresh = async () => {
  console.log(await desktop.helloworld())
}
refresh()


/* === 子组件 === */
import Menu from './Widget/Left1stMenu.vue'
import List from './Widget/Left2ndList.vue'
import Info from './Widget/RightInfo.vue'
</script>


<template>
<div class="container">

  <div class="left">
    <Menu class="menu" :options="['部件1', '部件2', '部件3']"/>
    <List class="list"/>
  </div>

  <div class="right">
    <Info class="info"/>
  </div>

</div>
</template>


<style lang="less" scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.container {
  width: 100%;
  height: 100%;
  padding: 0 10px 5px 10px;

  display: flex;
  justify-content: space-between;
  gap: 5px;

  .left {
    width: 25%;
    height: 100%;

    display: flex;
    flex-direction: column;
    gap: 5px;

    :nth-child(2) {
      flex: 1;
    }
  }
  .right {
    width: 75%;
    height: 100%;
  }
}
</style>
