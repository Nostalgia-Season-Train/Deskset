<script setup>
import { ElIcon } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { getDesksetReq } from '../request'

const open_recycle = async () => {
  const desksetReq = await getDesksetReq()
  desksetReq.get('/v0/quick/open-recycle')
}
</script>


<template>
<div class="button" @click="open_recycle">
  <el-icon size="30px" style="color: white;"><Delete /></el-icon>
</div>
</template>


<style scoped>
.button {
  display: flex;
  background-color: #FFFFFF01;
}
.button:active {
  background-color: rgba(158, 158, 158, 0.5);
}
</style>
