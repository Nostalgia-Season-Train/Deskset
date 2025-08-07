<script lang="ts" setup>
/* === 子组件 === */
import ElScrollbar from '#element-plus/ElScrollbar.vue'
import { Plus } from 'lucide-vue-next'
import Button from '#desksetui/Button.vue'


/* === 选项 === */
import { ref } from 'vue'

const options = ref<string[]>()


/* === 菜单 === */
import { onUnmounted } from 'vue'
import { getWidgetNameList } from '#manager/main/widget'
import { inlineWidgetList, prefixMark } from '#widget/register'

const isOpen = ref(false)  // 是否打开 Menu

const openMenu = async () => {
  if (isOpen.value) return  // 防止重复挂载 closeMenu
  options.value = [...inlineWidgetList, ...await getWidgetNameList()]
  isOpen.value = true
  setTimeout(() => document.addEventListener('click', closeMenu), 100)
}

const closeMenu = () => {
  isOpen.value = false
  document.removeEventListener('click', closeMenu)
}

onUnmounted(() => { if (isOpen.value) closeMenu() })  // 一并卸载 closeMenu
</script>


<template>
<div class="dropdown">

  <div @click="openMenu">
    <Button :width="'100%'"><Plus/></Button>
  </div>

  <div v-if="isOpen" class="menu">
    <ElScrollbar>
      <div v-for="option in options" @click="$emit('select', option)" class="option">
        {{ option.startsWith(prefixMark) ? option.replace(prefixMark, '') : option }}
      </div>
    </ElScrollbar>
  </div>

</div>
</template>


<style lang="less" scoped>
.dropdown {
  position: relative;

  .menu {
    position: absolute;
    z-index: 1;
    width: 100%;
    height: calc(22.4px * 16);  // 22.4px 是单个选项的高度

    // ElScrollbar 高度自适应
    overflow: hidden;

    .option {
      color: #FFF;
      background-color: #000C;
      &:hover {
        background-color: #333C;
      }
    }
  }
}
</style>
