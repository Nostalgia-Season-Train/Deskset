<script lang="ts" setup>
import Profile from './Profile.vue'
import Greet from './Greet.vue'
import StarNote from './StarNote.vue'
import CronTask from './CronTask.vue'
</script>


<template>
<div>

  <!-- 仓库资料 -->
    <!-- 第一部分是基本信息，包含头像、昵称和签名 -->
    <!-- 第二部分是数据统计，分别代表该 Obsidian 仓库的使用天数、笔记数量、附件数量 -->
  <Profile />

  <Greet />

  <StarNote />

  <CronTask />

</div>
</template>


<style lang="less" scoped>
</style>
