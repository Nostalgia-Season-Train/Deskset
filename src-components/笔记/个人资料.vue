<script lang="ts" setup>
import { ref } from 'vue'

const profile = ref({
  avatar: '',
  name: '昵称',
  bio: '签名'
})
// - avatar 头像
// - name   昵称
// - bio    签名
// - [ ] 统计
// - [ ] 链接（其他网站的资料）
// - [ ] 成就


// 配置
const config = defineModel({ type: Object })
const { themeName, getAsset } = defineProps(['themeName', 'getAsset'])

if (Object.keys(config.value).length != 0) {
  profile.value = config.value
  profile.value.avatar = await getAsset(themeName, profile.value.avatar)
}
</script>


<template>
<div class="profile">
  <div class="left">
    <div class="avatar">
      <img :src="profile?.avatar" draggable="false"></img>
    </div>
  </div>
  <div class="right">
    <div class="name">{{ profile.name }}</div>
    <div class="bio">{{ profile.bio }}</div>
  </div>
</div>
</template>


<style lang="less" scoped>
.profile {
  width: 280px;
  background-color: #FFF7;

  border: 1px solid white;
  border-radius: 5px;

  padding: 5px;

  display: flex;
  justify-content: space-between;
  gap: 5px;

  .avatar {
    width: 100px;
    height: 100px;
    background-color: white;
    img {
      width: 100%;
      height: 100%;
    }
  }
  .right {
    flex: 1;
    color: #FFF;
    .name {
      font-size: 20px;
    }
    .bio {
      margin-top: 5px;
    }
  }
}
</style>
