<script setup>
import { ElScrollbar, ElButton, ElIcon, ElInput } from 'element-plus'
import Update from './Setting/Update.vue'
</script>


<template>
<el-scrollbar>

  <Update />

</el-scrollbar>
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
