<script lang="ts" setup>
import { ref } from 'vue'

const base = ref({
  avatar: '',
  name: '昵称',
  bio: '签名'
})

const stats = ref({
  dayNum: 0,
  noteNum: 0,
  attachNum: 0
})
</script>


<template>
<div class="profile">

  <div class="base"><!-- 基本信息 -->
    <div class="avatar"><img :src="base.avatar"/></div>
    <div class="name">{{ base.name }}</div>
    <div class="bio">{{ base.bio }}</div>
  </div>

  <div class="stats"><!-- 仓库统计 -->
    <div class="data">
      <div>天数</div><div>{{ stats.dayNum }}</div>
    </div>
    <div class="data">
      <div>笔记</div><div>{{ stats.noteNum }}</div>
    </div>
    <div class="data">
      <div>附件</div><div>{{ stats.attachNum }}</div>
    </div>
  </div>

  <div class="open-vault">打开仓库</div>

</div>
</template>


<style lang="less" scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.profile {
  position: relative;
  width: 160px;
  padding: 5px;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;

  .base {
    display: flex;
    flex-direction: column;
    align-items: center;

    .avatar {
      width: 70px;
      height: 70px;
      img {
        width: 100%;
        height: 100%;
      }
    }
    .name {
      color: #FFF;
    }
    .bio {
      color: #FFFA;
    }
  }
  .stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 5px;

    .data {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  }
}
</style>
