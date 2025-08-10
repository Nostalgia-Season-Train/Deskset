<script lang="ts" setup>
import { config, axios } from '#manager/global'
import {
  DEFAULT_SERVER_PORT,
  DEFAULT_USERNAME,
  DEFAULT_PASSWORD
} from '#manager/global'

const updateServerPort = async () => {
  try {
    // @ts-ignore
    if (config.server_port == '') {
      config.server_port = (await axios.get('/v0/config/server-port')).data.result
      return
    }
    config.server_port = (await axios.post(
      '/v0/config/server-port',
      new URLSearchParams({ server_port: String(config.server_port) }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    )).data.result
  } catch {
    config.server_port = DEFAULT_SERVER_PORT
  }
}

const updateUsername = async () => {
  try {
    if (config.username == '') {
      config.username = (await axios.get('/v0/config/username')).data.result
      return
    }
    config.username = (await axios.post(
      '/v0/config/username',
      new URLSearchParams({ username: String(config.username) }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    )).data.result
  } catch {
    config.username = DEFAULT_USERNAME
  }
}

const updatePassword = async () => {
  try {
    if (config.password == '') {
      config.password = (await axios.get('/v0/config/password')).data.result
      return
    }
    config.password = (await axios.post(
      '/v0/config/password',
      new URLSearchParams({ password: String(config.password) }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }
    )).data.result
  } catch {
    config.password = DEFAULT_PASSWORD
  }
}

/* === 子组件 === */
import Input from '#shadcn/components/ui/input/Input.vue'
</script>


<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">端口</div>
      <div class="description">配置服务器端口（需要重启应用）</div>
    </div>
    <div class="right">
      <Input style="width: 120px;" v-model="config.server_port" @change="updateServerPort"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">用户名</div>
      <div class="description">配置服务器用户名</div>
    </div>
    <div class="right">
      <Input style="width: 120px;" v-model="config.username" @change="updateUsername"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">密码</div>
      <div class="description">配置服务器密码</div>
    </div>
    <div class="right">
      <Input style="width: 120px;" v-model="config.password" @change="updatePassword"/>
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.option {
  margin: 0 10px 0 10px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  .left {
    .name {
      font-size: 16px;
      color: var(--color-deskset-primary);
    }
    .description {
      font-size: 14px;
      color: var(--color-deskset-secondary);
    }
  }
}
</style>
