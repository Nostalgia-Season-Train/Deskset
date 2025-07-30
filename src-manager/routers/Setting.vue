<script setup>
import Update from './Setting/Update.vue'

/* === 子组件 === */
import ElScrollbar from '#element-plus/ElScrollbar.vue'
import Divider from '#desksetui/Divider.vue'
</script>


<template>
<ElScrollbar>

  <Divider>软件更新</Divider>
  <Update />

</ElScrollbar>
</template>


<style scoped>
.option {
  margin: 10px 10px 0 10px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.option>.word>.name {
  font-size: 16px;
  color: black;
}
.option>.word>.description {
  font-size: 14px;
  color: gray;
}
</style>
