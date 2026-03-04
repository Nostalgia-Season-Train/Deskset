<script lang="ts" setup>
import { ref } from 'vue'
import desktop from '#manager/global/page/desktop'
import { activeWidgetMap } from '#manager/global'

const desktopInfo = ref({
  width: 0,
  height: 0,
  dpr: 0
})

const refresh = async () => {
  desktopInfo.value = await desktop.getWindowData()
}
refresh()
</script>


<template>
<div class="desktop-info">

  <div class="item">
    <div>桌面宽高</div>
    <div>{{ desktopInfo.width }}*{{ desktopInfo.height }}</div>
  </div>

  <div class="item">
    <div>桌面 DPI</div>
    <div>{{ desktopInfo.dpr }}</div>
  </div>

  <div class="item">
    <div>部件数量</div>
    <div>{{ activeWidgetMap.size }}</div>
  </div>

</div>
</template>


<style lang="less" scoped>
.desktop-info {
  width: fit-content;
  height: fit-content;
  display: flex;
  justify-content: space-between;
  gap: 5px;
  .item {
    width: 100px;
    background: var(--bg);
  }
}
</style>
