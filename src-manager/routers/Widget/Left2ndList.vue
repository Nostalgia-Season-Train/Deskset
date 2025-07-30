<script lang="ts" setup>
import { activeWidgetMap } from '#manager/global'


/* === 子组件 === */
import ElScrollbar from '#element-plus/ElScrollbar.vue'
</script>


<template>
<div class="left2ndlist">
  <ElScrollbar>
    <div
      v-for="widget in Array.from(activeWidgetMap.values())"
      @click="$emit('select', widget.id)"
      class="item"
    >
      {{ widget.title }}
    </div>
  </ElScrollbar>
</div>
</template>


<style lang="less" scoped>
.left2ndlist {
  width: 100%;
  height: 100%;
  border: solid 1px rgba(#FFF, .3);

  // ElScrollbar 高度自适应
    // 注：left2ndlist 高度由父组件 flex 布局分配
  overflow: hidden;

  .item {
    color: #FFF;
    &:hover {
      background-color: #FFF3;
    }
  }
}
</style>
