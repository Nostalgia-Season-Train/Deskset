<template>
<div>

  <div class="option">
    <div class="left">
      <div class="name">开机启动</div>
      <div class="description">开机自动运行数字桌搭</div>
    </div>
    <div class="right">
      <!-- 后面补上下拉菜单 -->
    </div>
  </div>

  <div class="option">
    <div class="left">
      <div class="name">关闭行为</div>
      <div class="description">点击关闭按钮时，是否隐藏到托盘</div>
    </div>
    <div class="right">
      <!-- 后面补上下拉菜单 -->
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.option {
  margin: 0 10px 0 10px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  .left {
    .name {
      font-size: 16px;
      color: #FFF;
    }
    .description {
      font-size: 14px;
      color: #FFFA;
    }
  }
}
</style>
