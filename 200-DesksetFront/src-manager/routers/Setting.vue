<script lang="ts" setup>
import Common from './Setting/Common.vue'
import Server from './Setting/Server.vue'
import AI from './Setting/AI.vue'
import { ElScrollbar } from 'element-plus'
// - [ ] 临时
const isDevEnv = (import.meta as any).env.DEV as boolean
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

  <div class="item">
    <AI v-if="isDevEnv"/>
  </div>

</div>
</ElScrollbar>
</template>


<style lang="less" scoped>
@import '#manager/style.less';

.content {
  padding: 0 var(--content-padding);
  display: flex;
  flex-direction: column;

  .item>*:last-child {
    margin-bottom: 12px;
    padding: 5px;
    .deskset-layer-first();
  }
}
</style>
