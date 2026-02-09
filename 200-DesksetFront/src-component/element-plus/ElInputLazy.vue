<script lang="ts" setup>
import { ElInput } from 'element-plus'
import { ref, watch } from 'vue'

const model = defineModel()
const modelLocal = ref()
modelLocal.value = model.value

// 文字可能闪烁：考虑旧值 A，新值 B
  // modelLocal 向 model 异步赋值 B，modelLocal=B model=A
  // modelLocal 在异步赋值完成前读取 model，值变回 A，modelLocal=A model=A
  // model 异步赋值成功，反过来给 modelLocal 赋值 B，modelLocal=B model=B
const update = () => {
  model.value = modelLocal.value
  modelLocal.value = model.value
}
watch(model, () => modelLocal.value = model.value)
</script>


<template>
<ElInput
  v-model="modelLocal"
  @blur="update"
/>
</template>
