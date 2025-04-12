<script lang="ts" setup>
import { ref } from 'vue'
import { ElButton, ElDrawer, ElScrollbar } from 'element-plus'
import { SlidersHorizontal } from 'lucide-vue-next'

import Sidebar from './HomePage/Sidebar.vue'

const drawer = ref(false)
</script>


<template>
  <!-- 内容区 -->
  <el-scrollbar id="homepage-main" style="width: 100%; height: 100%; transform: translate(0, 0);">
    <el-button @click="drawer = true"><SlidersHorizontal /></el-button>
  </el-scrollbar>
  <!-- 侧边栏 -->
  <el-drawer v-model="drawer" direction="ltr" :with-header="false" append-to="#homepage-main">
    <Sidebar />
  </el-drawer>
</template>


<style lang="less" scoped>
::v-deep(.el-button) {
  padding: 8px;
}
</style>
