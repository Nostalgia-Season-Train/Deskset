<script lang="ts" setup>
import { ref } from 'vue'
import { ElSwitch } from 'element-plus'
import { floatManager } from '../child'

const isopen = ref(false)

const switchFloat = async () => {
  if (isopen.value) {
    floatManager.create('Diary', 240, 160)
  } else {
    floatManager.close('Diary')
  }
}
</script>


<template>
<div>
  <el-switch v-model="isopen" @click="switchFloat"></el-switch>
</div>
</template>
