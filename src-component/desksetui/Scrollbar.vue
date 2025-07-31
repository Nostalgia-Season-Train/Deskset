<template>
<div class="desksetui__scrollbar_container">
  <slot></slot>
</div>
</template>


<style scoped>
.desksetui__scrollbar_container { 
  height: 100%;

  /* 裁剪滚动 + 隐藏滚动条 */
  overflow: scroll;
  &::-webkit-scrollbar {
    display: none;
  }
}
</style>
