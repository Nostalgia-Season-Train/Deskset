<script lang="ts" setup>
import { ref } from 'vue'
import desktop from '#manager/global/page/desktop'

const desktopInfo = ref({
  width: 0,
  height: 0,
  dpr: 0
})

const refresh = async () => {
  desktopInfo.value = await desktop.getWindowData()
}
refresh()
</script>


<template>
<div>
  {{ desktopInfo }}
</div>
</template>
