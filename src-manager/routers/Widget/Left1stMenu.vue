<script lang="ts" setup>
/* === 子组件 === */
import { Plus } from 'lucide-vue-next'
import Button from '#manager/components/Button.vue'


/* === Props 声明 === */
import { defineProps } from 'vue'

defineProps<{ options: string[] }>()


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
    <div v-for="option in options" @click="$emit('select', option)" class="option">
      {{ option }}
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.dropdown {
  position: relative;

  .menu {
    position: absolute;
    width: 100%;

    .option {
      color: #FFF;
      background-color: #0007;
      &:hover {
        background-color: #FFF3;
      }
    }
  }
}
</style>
