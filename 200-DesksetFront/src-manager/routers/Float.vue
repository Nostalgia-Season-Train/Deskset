<script lang="ts" setup>
import { ElSwitch } from 'element-plus'
import { useFloatStore } from '#manager/main/float'

const store = useFloatStore()
</script>


<template>
<div>
  <ElSwitch v-model="store.diary"/>
</div>
</template>
