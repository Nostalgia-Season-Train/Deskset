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
      <div class="name">{{ _t('AI 基础 URL') }}</div>
      <div class="description">{{ _t('指定 API 服务地址 base_url') }}</div>
    </div>
    <div class="right">
      <InputLazy style="width: 150px;" v-model="store.ai_base_url"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('AI 密钥') }}</div>
      <div class="description">{{ _t('配置 API 密钥 api_key') }}</div>
    </div>
    <div class="right">
      <InputLazy style="width: 150px;" v-model="store.ai_api_key"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('AI 模型') }}</div>
      <div class="description">{{ _t('选择一个 AI 模型 model') }}</div>
    </div>
    <div class="right">
      <InputLazy style="width: 150px;" v-model="store.ai_model"/>
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
@import '#manager/style.less';

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
