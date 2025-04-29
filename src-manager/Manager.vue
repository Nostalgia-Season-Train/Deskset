<script lang="ts" setup>
/* === 组件 === */
import LeftNav from './Manager/LeftNav.vue'


/* === 路由 === */
import { useRouter } from 'vue-router'
const router = useRouter()
const jump = async (page: string) => {
  console.log(page)
}
</script>


<template>
<body>

  <!-- 侧边栏 -->
  <aside>
    <LeftNav @jump="jump"/>
  </aside>

</body>
</template>


<style lang="less" scoped>
* {
  margin: 0; padding: 0;
  user-select: none;
}
</style>
