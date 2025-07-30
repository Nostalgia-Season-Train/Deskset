<template>
<div class="w-full flex justify-center items-center">

  <div class="w-1/10"><!-- 左：10% -->
    <div class="w-full h-px bg-white"></div>
  </div>

  <div class="p-[5px] text-white">
    <slot></slot>
  </div>

  <div class="flex-1"><!-- 右：填满 -->
    <div class="w-full h-px bg-white"></div>
  </div>

</div>
</template>


<style scoped>
/* 样式采用 Tailwind CSS 编写 */
</style>
