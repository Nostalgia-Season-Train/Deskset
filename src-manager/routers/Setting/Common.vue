<script lang="ts" setup>
import { ref } from 'vue'

const isAutostart = ref(false)
const closeBehavior = ref('隐藏')

/* === 子组件 === */
import Switch from '#desksetui/Switch.vue'
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
      <Switch v-model="isAutostart"/>
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
          <Button>{{ closeBehavior }}</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56">
          <DropdownMenuRadioGroup v-model="closeBehavior">
            <DropdownMenuRadioItem value="隐藏">最小化到系统托盘</DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="退出">退出应用</DropdownMenuRadioItem>
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
