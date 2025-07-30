<script lang="ts" setup>
withDefaults(defineProps<{
  placeholder?: string
}>(), {
  placeholder: 'Type here'
})
const model = defineModel()
</script>


<template>
<div class="input-container">
  <input
    class="input" type="text" :placeholder="placeholder"
    v-model="model"
  />
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
  background: none;
  border: none;
  &::placeholder {
    color: #FFFA;  // 占位文本色
  }
  &:focus {
    outline: none;
  }
  &::selection {
    color: inherit;  // 选中文字色：保持不变
    background: #FFF1;  // 选中背景色
  }
}

// 自定义属性
.input-container {
  --color: #FFF;
  --bottom-border-height: 1px;
}

.input-container {
  position: relative;

  width: 160px;
  height: 28px;
  border: solid 1px rgba(from var(--color) r g b / .3);

  transition: .3s ease;
  &:hover {
    box-shadow: 0 0 5px 0 rgba(from var(--color) r g b / .1);
    border-color: rgba(from var(--color) r g b / .5);
  }

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
