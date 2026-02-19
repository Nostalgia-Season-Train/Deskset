<script lang="ts" setup>
const emit = defineEmits(['change'])
const NoteGroup = defineModel({ required: true })
console.log(NoteGroup.value)
</script>


<template>
<div>
  笔记分组
</div>
</template>
