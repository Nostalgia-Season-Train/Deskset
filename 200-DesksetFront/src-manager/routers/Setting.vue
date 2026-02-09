<script lang="ts" setup>
import Common from './Setting/Common.vue'
import Server from './Setting/Server.vue'
import { ElScrollbar } from 'element-plus'
</script>


<template>
<ElScrollbar>
<div class="content">

  <div class="item">
    <Common/>
  </div>

  <div class="item">
    <Server/>
  </div>

</div>
</ElScrollbar>
</template>


<style lang="less" scoped>
.content {
  padding: 0 var(--content-padding);
  display: flex;
  flex-direction: column;

  .item>*:last-child {
    margin-bottom: 12px;
    padding: 5px;
    background: var(--bg);
  }
}
</style>
