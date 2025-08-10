<script lang="ts" setup>
/* === 子组件 === */
import { Plus } from 'lucide-vue-next'
import Button from '#shadcn/components/ui/button/Button.vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '#shadcn/components/ui/dropdown-menu'


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

  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button class="w-full" @click="openMenu"><Plus/></Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent class="w-full">
      <DropdownMenuItem v-for="option in options" @click="$emit('select', option)">
        {{ option.startsWith(prefixMark) ? option.replace(prefixMark, '') : option }}
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

</div>
</template>
