<script lang="ts" setup>
import { _t } from '#manager/main/i18n'

/* === 子组件 === */
import {
  ElButton,
  ElSwitch,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem
} from 'element-plus'


/* ==== [ ] 测试中 Pinia ==== */
import { useConfigStore } from '#manager/main/config'

const store = useConfigStore()
</script>


<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('语言') }}</div>
      <div class="description">{{ _t('选择界面语言') }}<span class="info">需要重启</span></div>
    </div>
    <div class="right">
      <ElDropdown placement="bottom-end" trigger="click">
        <ElButton>{{ store.language == 'zh-cn' ? '中文' : 'English' }}</ElButton>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem @click="store.language = 'zh-cn'">中文</ElDropdownItem>
            <ElDropdownItem @click="store.language = 'en'">English</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('开机启动') }}</div>
      <div class="description">{{ _t('是否开机自动运行') }}</div>
    </div>
    <div class="right">
      <ElSwitch v-model="store.isAutostart"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('关闭行为') }}</div>
      <div class="description">{{ _t('点击关闭按钮时，是隐藏窗口还是直接退出') }}</div>
    </div>
    <div class="right">
      <ElDropdown placement="bottom-end" trigger="click">
        <ElButton>{{ store.closeBehavior == 'hide' ? _t('隐藏') : _t('退出') }}</ElButton>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem @click="store.closeBehavior = 'hide'">{{ _t('最小化到系统托盘') }}</ElDropdownItem>
            <ElDropdownItem @click="store.closeBehavior = 'exit'">{{ _t('退出应用') }}</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>
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
