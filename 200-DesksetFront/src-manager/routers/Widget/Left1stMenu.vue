<script lang="ts" setup>
import { _t } from '#manager/main/i18n'

/* === 子组件 === */
import { Plus } from 'lucide-vue-next'
import {
  ElButton,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem
} from 'element-plus'


/* === 选项 === */
import { ref } from 'vue'

const options = ref<string[]>()


/* === 菜单 === */
import { getWidgetNameList } from '#manager/main/widget'
import { inlineWidgetList, prefixMark } from '#widget/register'

const openMenu = async () => {
  options.value = [...inlineWidgetList, ...await getWidgetNameList()]
}
</script>


<template>
<div class="dropdown">

  <ElDropdown placement="bottom" trigger="click" style="width: 100%; height: 100%;">
    <ElButton @click="openMenu">
      <Plus/>
      <span>添加部件</span>
    </ElButton>
    <template #dropdown>
      <!-- 固定宽度，v-for 第一次渲染宽度为零，菜单右偏 -->
      <ElDropdownMenu
        style="max-height: 80vh; width: 150px; min-width: 150px; max-width: 150px;"
      >
        <ElDropdownItem v-for="option in options" @click="$emit('select', { name: option })">
          {{ option.startsWith(prefixMark) ? _t(option.replace(prefixMark, '')) : option }}
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>

</div>
</template>


<style lang="less" scoped>
.dropdown {
  .el-button {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    svg {
      stroke-width: 1;
    }
  }
}
</style>
