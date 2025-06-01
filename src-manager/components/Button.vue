<template>
<div class="button-container">
  <div class="button">
    <div class="slot-area">
      <slot></slot><!-- 使用方法：<Button>插槽内容</Button>，插槽内容 替换 <slot></slot> -->
    </div>
  </div>
</div>
</template>


<style lang="less" scoped>
.button-container {
  --color: #FFF;

  .button {
    box-sizing: border-box;
    width: 56px;
    height: 28px;
    border: solid 1px rgba(from var(--color) r g b / .3);

    display: flex;
    justify-content: center;
    align-items: center;

    cursor: pointer;

    transition: .3s ease;
    &:hover {
      box-shadow: 0 0 5px 0 rgba(from var(--color) r g b / .1);
      border-color: rgba(from var(--color) r g b / .5);
    }
    &:active {
      background: rgba(from var(--color) r g b / .1);
    }

    .slot-area {
      width: 15px;
      height: 15px;

      display: flex;
      justify-content: center;
      align-items: center;

      color: #FFF;
      font-size: 14px;

      // 宽高太小，允许溢出不换行
      overflow: visible;
      white-space: nowrap;

      svg {
        width: 100%;
        height: 100%;
      }
    }
  }
}
</style>
