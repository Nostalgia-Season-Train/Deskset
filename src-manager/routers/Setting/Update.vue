<script lang="ts" setup>
/* === Element Plus === */
import { ElButton, ElIcon, ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'


/* === 获取软件更新 === */
import { Octokit } from 'octokit'

const octokit = new Octokit({
  // auth: import.meta.env.VITE_DESKSET_GITHUB_TOKEN  // 好像不需要 token
})

const getReleasesLatest = async () => {
  try {
    const rep = await octokit.request('GET /repos/{owner}/{repo}/releases/latest', {
      owner: 'Nostalgia-Season-Train',
      repo: 'Deskset'
    })
    ElMessage({
      type: 'success',
      message: `检测到最新版本 ${rep.data.name}`
    })
  } catch (error) {
    ElMessage({
      type: 'error',
      message: `错误！${error}`
    })
  }
}
</script>


<template>
<div class="option"><!-- 由父组件定义 option 样式 -->
  <div class="left">
    <div class="name">软件更新</div>
    <div class="description">检查数字桌搭最新版本</div>
  </div>
  <div class="right">
    <el-button type="primary" @click="getReleasesLatest">
      <el-icon style="margin: 0;"><Refresh /></el-icon>
    </el-button>
  </div>
</div>
</template>


<style lang="less" scoped>
.left {
  .name {
    font-size: 16px;
    color: black;
  }
  .description {
    font-size: 14px;
    color: gray;
  }
}
</style>
