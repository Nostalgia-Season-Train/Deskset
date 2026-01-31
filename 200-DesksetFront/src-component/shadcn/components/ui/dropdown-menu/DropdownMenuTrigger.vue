<script setup lang="ts">
import { DropdownMenuTrigger, type DropdownMenuTriggerProps, useForwardProps } from 'reka-ui'

const props = defineProps<DropdownMenuTriggerProps>()

const forwardedProps = useForwardProps(props)
</script>

<template>
  <DropdownMenuTrigger
    class="dropdown-menu-trigger"
    data-slot="dropdown-menu-trigger"
    v-bind="forwardedProps"
  >
    <slot />
  </DropdownMenuTrigger>
</template>

<style scoped lang="less">
.dropdown-menu-trigger {
  font-size: var(--text-size);
  background: var(--bg-light);
  border: none;
  box-shadow: none;

  transition: .3s;

  &:hover {
    box-shadow: var(--shadow-s);
  }
  &:active {
    box-shadow: none;
  }
}
</style>
