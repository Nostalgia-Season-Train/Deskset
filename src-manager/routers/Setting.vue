<script setup>
import Common from './Setting/Common.vue'
import Server from './Setting/Server.vue'
import Update from './Setting/Update.vue'

/* === 子组件 === */
import ElScrollbar from '#element-plus/ElScrollbar.vue'
import Divider from '#desksetui/Divider.vue'
</script>


<template>
<ElScrollbar>

  <Divider>通用选项</Divider>
  <Common/>

  <Divider>服务器配置</Divider>
  <Server/>

  <Divider>软件更新</Divider>
  <Update/>

</ElScrollbar>
</template>
