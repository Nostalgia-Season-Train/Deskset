<script lang="ts" setup>
import { ref } from 'vue'

const port = ref<number>(6527)
const username = ref<string>('username')
const password = ref<string>('password')

/* === 子组件 === */
import Input from '#desksetui/Input.vue'
</script>


<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">端口</div>
      <div class="description">配置服务器端口（需要重启应用）</div>
    </div>
    <div class="right">
      <Input style="width: 120px;" v-model="port"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">用户名</div>
      <div class="description">配置服务器用户名</div>
    </div>
    <div class="right">
      <Input style="width: 120px;" v-model="username"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">密码</div>
      <div class="description">配置服务器密码</div>
    </div>
    <div class="right">
      <Input style="width: 120px;" v-model="password"/>
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
      color: #FFF;
    }
    .description {
      font-size: 14px;
      color: #FFFA;
    }
  }
}
</style>
