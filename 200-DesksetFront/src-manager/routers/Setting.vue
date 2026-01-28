<script setup>
import { _t } from '#manager/main/i18n'
import Common from './Setting/Common.vue'
import Server from './Setting/Server.vue'

/* === 子组件 === */
import Scrollbar from '#desksetui/Scrollbar.vue'
// import Divider from '#desksetui/Divider.vue'
</script>


<template>
<Scrollbar>
<div class="content">

  <div class="item">
    <!-- <Divider>{{ _t('通用选项') }}</Divider> -->
    <Common/>
  </div>

  <div class="item">
    <!-- <Divider>{{ _t('服务器配置') }}</Divider> -->
    <Server/>
  </div>

</div>
</Scrollbar>
</template>


<style lang="less" scoped>
.content {
  padding: 0 var(--content-padding);
  display: flex;
  flex-direction: column;

  // .item>*:first-child {
  //   font-size: var(--text-sharp-size);
  // }
  .item>*:last-child {
    margin-bottom: 12px;
    padding: 5px;
    background: var(--bg);
  }
}
</style>
