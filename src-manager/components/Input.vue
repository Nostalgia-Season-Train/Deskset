<template>
<div class="input-container">
  <input class="input" type="text" placeholder="Type here"/>
  <span class="bottom-border"></span>
</div>
</template>


<style lang="less" scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

// 去掉输入框 input 默认样式
input {
  border: none;
  &:focus {
    outline: none;
  }
  &::selection {
    color: inherit;  // 选中文字色：保持不变
    background: #FFF1;  // 选中背景色
  }
}

.input-container {
  position: relative;

  width: 160px;
  height: 32px;

  --bottom-border-height: 1px;

  .input {
    position: absolute;
    top: 0;
    left: 0;

    width: 100%;
    height: calc(100% - var(--bottom-border-height));
    padding: 4px;
    padding-left: 8px;

    // 输入文字样式
    color: #FFF;
    font-size: 16px;

    background: transparent;
    box-shadow: 4px 4px 8px rgba(0,0,0,.2);
  }
  .bottom-border {
    position: absolute;
    bottom: 0;
    left: 0;

    width: 0%;
    height: var(--bottom-border-height);

    background: linear-gradient(90deg, #FFF5 0%, #FFFA 100%);

    transition: .4s ease-in-out;
  }
  .input:focus+.bottom-border {
    width: 100%;
  }
}
</style>
