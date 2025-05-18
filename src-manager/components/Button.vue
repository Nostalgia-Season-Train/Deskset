<template>
<div class="button-container">
  <div class="button">
    <div class="text">按钮</div>
  </div>
</div>
</template>


<style lang="less" scoped>
.button-container {
  --color: #FFF;

  .button {
    box-sizing: border-box;
    width: 80px;
    height: 30px;
    border: solid 1px rgba(from var(--color) r g b / .1);

    display: flex;
    justify-content: center;
    align-items: center;

    color: #FFF;
    font-size: 16px;

    cursor: pointer;

    transition: .3s ease;
    &:hover {
      box-shadow: 0 0 5px 0 rgba(from var(--color) r g b / .25);
    }
    &:active {
      border-color: rgba(from var(--color) r g b / .5);
    }
  }
}
</style>
