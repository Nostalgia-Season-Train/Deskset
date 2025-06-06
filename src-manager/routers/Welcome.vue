<script lang="ts" setup>
import { ElScrollbar } from 'element-plus'

import { openBrowser } from '#manager/tauri.ts'
const openReleasePage = () => {
  openBrowser("https://github.com/Nostalgia-Season-Train/Deskset")
}
</script>


<template>
<el-scrollbar>
<div class="container">

  <div class="center">
    <div>
      <img src="/static/icons/Deskset.png" width="100px"></img>
    </div>
    <div>欢迎使用数字桌搭 Deskset</div>
    <div>一款桌面美化软件</div>
    <div>基于 Web 技术开发</div>
    <div>实现桌面美化与笔记应用间的互动</div>
  </div>

  <h2>介绍</h2>
  <div>数字桌搭是一款专注整合笔记应用的桌面美化软件，旨在优化笔记的读写管理流程，从而提高个人生产力。</div>

  <h2>主要功能</h2>
  <div>主页：以博客形式可视化笔记仓库</div>
  <div class="br"></div>

  <div>组件：桌面美化小部件</div>
  <ul>
    <li>设备：提供系统监控卡片，实时测量芯片、内存信息</li>
    <li>快速启动：Mac 风格菜单，更好的回收站图标</li>
    <li>时间：多种样式的时钟，计时器，番茄钟</li>
    <li>笔记：放置喜欢的笔记在桌面上</li>
  </ul>
  <div class="br"></div>

  <div>主题：轻松保存和应用主题，并通过 CSS 定制样式</div>

  <h2>发布 & 交流</h2>
  <div>项目地址：<a @click="openReleasePage()" @click.prevent href="#">数字桌搭 - Deskset</a></div>
  <div>QQ 群：770889923</div>

</div>
</el-scrollbar>
</template>


<style lang="less" scoped>
/* 去掉滚动条 */
:deep(.el-scrollbar__thumb) {
  display: none;
}

.container {
  padding: 0 10px;
  color: white;

  .center {
    text-align: center;
  }
  h2 {
    margin: 1em 0 0 0;
    font-size: 1.25em;
  }
  .br {
    margin: 0.5em;
  }
  ul {
    margin: 0 0 0 2em;
    padding: 0;
  }
  a {
    color: gray;
    text-decoration: none;
  }
}
</style>
