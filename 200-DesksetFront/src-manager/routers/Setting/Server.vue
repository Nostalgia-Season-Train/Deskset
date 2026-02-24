<script lang="ts" setup>
import { _t } from '#manager/main/i18n'

/* === 子组件 === */
import InputLazy from '#element-plus/ElInputLazy.vue'


/* ==== [ ] 测试中 Pinia ==== */
import { useConfigStore } from '#manager/main/config'

const store = useConfigStore()
</script>


<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('端口') }}</div>
      <div class="description">{{ _t('配置服务器端口') }}<span class="info">需要重启</span></div>
    </div>
    <div class="right">
      <InputLazy style="width: 150px;" v-model="store.server_port"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('用户名') }}</div>
      <div class="description">{{ _t('配置服务器用户名') }}</div>
    </div>
    <div class="right">
      <InputLazy style="width: 150px;" v-model="store.username"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('密码') }}</div>
      <div class="description">{{ _t('配置服务器密码') }}</div>
    </div>
    <div class="right">
      <InputLazy style="width: 150px;" v-model="store.password"/>
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
      .deskset-text-title();
    }
    .description {
      .deskset-text();
      .info {
        .deskset-text-caption();
      }
    }
  }
}
</style>
