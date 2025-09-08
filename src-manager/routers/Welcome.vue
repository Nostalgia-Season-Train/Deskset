<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import Scrollbar from '#desksetui/Scrollbar.vue'

import { openBrowser } from '#manager/main/tauri'
const openReleasePage = () => {
  openBrowser("https://github.com/Nostalgia-Season-Train/Deskset")
}
</script>


<template>
<Scrollbar>
<div class="container-welcome">

  <div class="center">
    <div>
      <img src="/static/icons/Deskset.png" width="100px"></img>
    </div>
    <div>{{ _t('欢迎使用数字桌搭 Deskset') }}</div>
    <div>{{ _t('一款桌面美化软件') }}</div>
    <div>{{ _t('基于 Web 技术开发') }}</div>
    <div>{{ _t('定制专属于你的高效工作台') }}</div>
  </div>

  <h2>{{ _t('介绍') }}</h2>
  <div>{{ _t('数字桌搭是一款开源的桌面美化应用，拥有多个美化部件。通过覆盖原始桌面，允许用户创建自己的个性化桌面，并能保存为主题后分享给其他人。') }}</div>
  <div>{{ _t('除此之外，数字桌搭还拥有强大的插件系统：') }}
    <ul>
      <li>{{ _t('支持导入单个 vue 文件作为桌面部件') }}</li>
      <li>{{ _t('支持导入 py 模块以给部件提供数据接口') }}</li>
    </ul>
  </div>

  <!-- <h2>主要功能</h2>
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

  <div>主题：轻松保存和应用主题，并通过 CSS 定制样式</div> -->

  <h2></h2>
  <div>{{ _t('项目地址：') }}<a @click="openReleasePage()" @click.prevent href="#">{{ _t('数字桌搭 - Deskset') }}</a></div>
  <!-- <div>QQ 群：770889923</div> -->

</div>
</Scrollbar>
</template>


<style lang="less" scoped>
// 若类名等于 container，则无法填满 content，原因未知
.container-welcome {
  padding: 0 10px;
  color: var(--color-deskset-primary);

  .center {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  h2 {
    margin: 0.5em 0 0 0;
    font-size: 1.25em;
  }
  .br {
    margin: 0.5em;
  }
  ul {
    list-style-type: disc;
    margin: 0 0 0 1.5em;
    padding: 0;
  }
  a {
    color: var(--color-deskset-secondary);
    text-decoration: none;
  }
}
</style>
