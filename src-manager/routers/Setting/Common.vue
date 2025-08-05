<script lang="ts" setup>
import { config } from '#manager/global'
import { enable, disable, isEnabled } from '@tauri-apps/plugin-autostart'

const switchAutostart = async () => {
  if (config.isAutostart) {
    await disable()
    config.isAutostart = await isEnabled()
  } else {
    await enable()
    config.isAutostart = await isEnabled()
  }
}

/* === 子组件 === */
import SwitchBrief from '#desksetui/SwitchBrief.vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger
} from '#shadcn/components/ui/dropdown-menu'
import Button from '#desksetui/Button.vue'
</script>


<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">开机启动</div>
      <div class="description">是否开机自动运行</div>
    </div>
    <div class="right">
      <SwitchBrief v-model="config.isAutostart" @click="switchAutostart"/>
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">关闭行为</div>
      <div class="description">点击关闭按钮时，是隐藏窗口还是直接退出</div>
    </div>
    <div class="right">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button>{{ config.closeBehavior == 'hide' ? '隐藏' : '退出' }}</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56">
          <DropdownMenuRadioGroup v-model="config.closeBehavior">
            <DropdownMenuRadioItem value="hide">最小化到系统托盘</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="exit">退出应用</DropdownMenuRadioItem>
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
      color: #FFF;
    }
    .description {
      font-size: 14px;
      color: #FFFA;
    }
  }
}
</style>
