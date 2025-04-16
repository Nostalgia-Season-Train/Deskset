<script lang="ts" setup>
import { ref } from 'vue'

const profile = ref({
  avatar: '',
  name: '昵称',
  bio: '签名'
})
const avatarSrc = ref()
// - avatar 头像
// - name   昵称
// - bio    签名
// - [ ] 统计
// - [ ] 链接（其他网站的资料）
// - [ ] 成就


/* === 刷新 === */
import { inject } from 'vue'
import { Axios } from 'axios'

const axios = inject('$axios') as Axios
const refresh = async () => {
  avatarSrc.value = URL.createObjectURL((await axios.get('/v0/note/obsidian/profile/avatar', {
    responseType: 'blob',
    params: { t: new Date() }  // 强制显示新图片
  })).data)
  profile.value = (await axios.get('/v0/note/obsidian/profile/data')).data.result
}
refresh()
</script>


<template>
<div class="profile">
  <div class="left">
    <img class="avatar" :src="avatarSrc" draggable="false"></img>
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
  background-color: #FFF3;

  border-radius: 5px;

  display: flex;
  justify-content: space-between;

  .left {
    width: 100px;
    height: 100px;
    background-color: white;

    .avatar {
      width: 100%;
      height: 100%;
    }
  }

  .right {
    flex: 1;
    color: #FFF;

    margin: 5px;

    display: flex;
    flex-direction: column;
    gap: 3px;

    .name {
      font-size: 16px;
      font-weight: bold;
    }
    .bio {
      font-size: 14px;
    }
  }
}
</style>
