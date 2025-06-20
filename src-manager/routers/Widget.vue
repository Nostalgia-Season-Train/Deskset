<script lang="ts" setup>
import desktop from '#manager/broadcast/desktop'

const refresh = async () => {
  console.log(await desktop.helloworld())
}
refresh()
</script>


<template>
</template>


<style lang="less" scoped>
</style>
