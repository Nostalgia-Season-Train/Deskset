<script lang="ts" setup>
import { _t } from '#manager/main/i18n'

/* === 子组件 === */
import SwitchBrief from '#shadcn/components/ui/switch/Switch.vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger
} from '#shadcn/components/ui/dropdown-menu'
import Button from '#shadcn/components/ui/button/Button.vue'


/* ==== [ ] 测试中 Pinia ==== */
import { useConfigStore } from '#manager/main/config'

const store = useConfigStore()
</script>


<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('语言') }}</div>
      <div class="description">{{ _t('选择界面语言（需要重启）') }}</div>
    </div>
    <div class="right">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button>{{ store.language == 'zh-cn' ? '中文' : 'English' }}</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-50">
          <DropdownMenuRadioGroup v-model="store.language">
            <DropdownMenuRadioItem value="zh-cn">中文</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="en">English</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('开机启动') }}</div>
      <div class="description">{{ _t('是否开机自动运行') }}</div>
    </div>
    <div class="right">
      <SwitchBrief v-model="store.isAutostart"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">{{ _t('关闭行为') }}</div>
      <div class="description">{{ _t('点击关闭按钮时，是隐藏窗口还是直接退出') }}</div>
    </div>
    <div class="right">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button>{{ store.closeBehavior == 'hide' ? _t('隐藏') : _t('退出') }}</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-50">
          <DropdownMenuRadioGroup v-model="store.closeBehavior">
            <DropdownMenuRadioItem value="hide">{{ _t('最小化到系统托盘') }}</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="exit">{{ _t('退出应用') }}</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
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
