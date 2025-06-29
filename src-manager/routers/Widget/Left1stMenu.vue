<script lang="ts" setup>
/* === 子组件 === */
import { ElScrollbar } from 'element-plus'
import { Plus } from 'lucide-vue-next'
import Button from '#manager/components/Button.vue'


/* === Props 声明 === */
import { defineProps } from 'vue'

defineProps<{
  options: {
    local: string,
    type: string,
    name: string
  }[]
}>()


/* === 主函数 === */
import { ref, onUnmounted } from 'vue'

const isOpen = ref(false)  // 是否打开 Menu

const openMenu = () => {
  if (isOpen.value)
    return  // 防止重复挂载 closeMenu
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
    <el-scrollbar>
      <div v-for="option in options" @click="$emit('select', option.local)" class="option">
        {{ option.name }}
      </div>
    </el-scrollbar>
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
    :deep(.el-scrollbar__thumb) {
      display: none;
    }

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
