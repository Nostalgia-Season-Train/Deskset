<script setup>
import { _t } from '#manager/main/i18n'
import Common from './Setting/Common.vue'
import Server from './Setting/Server.vue'
import Update from './Setting/Update.vue'

/* === 子组件 === */
import Scrollbar from '#desksetui/Scrollbar.vue'
import Divider from '#desksetui/Divider.vue'
</script>


<template>
<Scrollbar>

  <Divider>{{ _t('通用选项') }}</Divider>
  <Common/>

  <Divider>{{ _t('服务器配置') }}</Divider>
  <Server/>

</Scrollbar>
</template>
