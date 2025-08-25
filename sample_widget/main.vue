<!-- 暂不支持 TypeScript 语法 -->
<script setup>
import { ref } from 'vue'
import { useInterval } from 'vue-hooks-plus'
import axios from 'axios'

const percent = ref(0)

// useInterval 组件卸载时停止轮询
useInterval(async () => {
  // Axios 使用事项：
    // 1、请求自动添加地址前缀 http://127.0.0.1:6527
    // 2、可在 http://127.0.0.1:6527/docs 查看 API 文档
    // 3、后端返回格式 {
    //   success: bool 是否成功
    //   code: int     错误码
    //   message: str  失败信息
    //   result: any   数据
    // }
  percent.value = (await axios.get('/v0/device/realtime')).data.result.cpu.percent
}, 1200)

// Element Plus 使用事项：
  // 1、Element Plus 组件需要显式导入
import { ElProgress } from 'element-plus'
</script>


<!-- 确保只有一个根节点 -->
<template>
<div class="progress">
  <el-progress :percentage="percent"/>
</div>
</template>


<style scoped>
.progress {
  width: 300px;
}
:deep(.el-progress__text) {
  color: black;
}
</style>
