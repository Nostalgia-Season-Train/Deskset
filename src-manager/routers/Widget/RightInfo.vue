<script lang="ts" setup>
import Button from '#manager/components/Button.vue'
import Switch from '#manager/components/SwitchBrief.vue'
</script>


<template>
<div class="rightinfo">

  <div class="top">
    <div class="title">标题（用户自定义）</div><!-- title -->
    <div class="name">名称（文件夹/文件）</div><!-- folder/file -->
    <div class="description">描述</div><!-- description -->
  </div>

  <div class="bottom">
    <div class="left">
      <div>
        <Button :width="'100%'">定位</Button>
      </div>
      <div>
        <div>坐标</div>
      </div>
    </div>

    <div class="right">
      <div class="option"><span>锁定拖动</span><Switch/></div>
      <div class="option"><span>禁用交互</span><Switch/></div>
      <div class="option"><span>自动隐藏</span><Switch :size="20.5"/></div><!-- 错觉？21px 比其他滑块大一点 -->
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.rightinfo {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  color: #FFF;

  .top {
    .title {
      height: 28px;

      display: flex;
      justify-content: flex-start;  // start、end、left、right 已弃用
      align-items: center;

      font-size: 20px;
      font-weight: 1000;
    }
    .name {
      margin-top: 1px;
    }
  }
  .bottom {
    height: 35%;

    display: flex;
    justify-content: space-between;
    align-items: stretch;  // 让子元素填满高度
    gap: 5px;

    .left {
      flex: 1;
    }
    .right {
      flex: 1;

      display: flex;
      flex-direction: column;
      gap: 5px;

      .option {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }
  }
}
</style>
