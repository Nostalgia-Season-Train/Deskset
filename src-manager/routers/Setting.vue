<script setup>
import Common from './Setting/Common.vue'
import Server from './Setting/Server.vue'
import Update from './Setting/Update.vue'

/* === 子组件 === */
import Scrollbar from '#desksetui/Scrollbar.vue'
import Divider from '#desksetui/Divider.vue'
</script>


<template>
<Scrollbar>

  <Divider>通用选项</Divider>
  <Common/>

  <Divider>服务器配置</Divider>
  <Server/>

  <Divider>软件更新</Divider>
  <Update/>

</Scrollbar>
</template>
