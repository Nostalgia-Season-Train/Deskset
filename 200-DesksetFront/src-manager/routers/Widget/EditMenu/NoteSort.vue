<script lang="ts" setup>
const emit = defineEmits(['change'])
const NoteSort = defineModel({ required: true })
console.log(NoteSort.value)
</script>


<template>
<div>
  笔记排序
</div>
</template>
