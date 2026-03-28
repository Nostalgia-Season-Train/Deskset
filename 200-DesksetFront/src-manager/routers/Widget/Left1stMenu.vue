<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
// - [ ] 临时：后面从父组件获取列表
import { useWidgetStore } from '#manager/main/widget'
const store = useWidgetStore()

/* === 子组件 === */
import { Grid2X2Plus } from 'lucide-vue-next'
import {
  ElButton,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem
} from 'element-plus'


/* === 选项 === */
import { ref } from 'vue'
import { Widgetcls } from '#manager/main/widget'

const options = ref<Widgetcls[]>()


/* === 菜单 === */
const openMenu = async () => {
  options.value = await store.getWidgetNameList()
}
</script>


<template>
<div class="dropdown">

  <ElDropdown placement="bottom" trigger="click" style="width: 100%; height: 100%;">
    <ElButton @click="openMenu">
      <Grid2X2Plus/>
      <span style="width: 3px;"></span>
      <span>添加部件</span>
    </ElButton>
    <template #dropdown>
      <!-- 固定宽度，v-for 第一次渲染宽度为零，菜单右偏 -->
      <ElDropdownMenu
        style="max-height: 80vh; width: 150px; min-width: 150px; max-width: 150px;"
      >
        <ElDropdownItem v-for="option in options" @click="$emit('select', {
          path: option.path, beInline: option.beInline
        })"><!-- [ ] 这里没有类型检查！？ -->
          {{ option.name }}
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
    svg {
      width: 20px;
      height: 20px;
      stroke-width: 1;
    }
  }
}
</style>
