<script lang="ts" setup>
import { Widget } from '#manager/global'

const widget = defineModel<Widget>({ required: true })


/* === 事件 === */
const emit = defineEmits([
  'remove',
  'switchProp'
])


/* === 子组件 === */
import Button from '#manager/components/Button.vue'
import Switch from '#manager/components/SwitchBrief.vue'
</script>


<template>
<div class="rightinfo">

  <div class="top">
    <div class="first-line">
      <div class="title">{{ widget.title }}</div>
      <div class="btns">
        <div class="btn"><Button @click="emit('remove', widget.id)">删除</Button></div>
        <div class="btn"><Button>编辑</Button></div>
        <div class="btn"><Button>定位</Button></div>
      </div>
    </div>
    <div class="name">{{ widget.name }}</div>
    <div class="author">{{ widget.author }}</div>
    <div class="version">{{ widget.version }}</div>
    <div class="descript">{{ widget.descript }}</div>
  </div>

  <div class="bottom">
    <div class="left">
      <div>
        <div class="flex">
          <span class="w-1/3 text-center">坐标</span>
          <span class="w-1/3 text-center">{{ widget.x }}</span>
          <span class="w-1/3 text-center">{{ widget.y }}</span>
        </div>
      </div>
    </div>

    <div class="right">
      <div class="option">
        <span>锁定拖动</span>
        <Switch v-model="widget.isDragLock" @click="emit('switchProp', widget.id, 'drag-lock', !widget.isDragLock)"/>
      </div>
      <div class="option">
        <span>禁用交互</span>
        <Switch v-model="widget.isDisableInteract" @click="emit('switchProp', widget.id, 'disable-interact', !widget.isDisableInteract)"/>
      </div>
      <div class="option">
        <span>自动隐藏</span>
        <Switch v-model="widget.isAutoHide" @click="emit('switchProp', widget.id, 'auto-hide', !widget.isAutoHide)" :size="20.5"/><!-- 错觉？21px 比其他滑块大一点 -->
      </div>
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
    .first-line {
      height: 28px;

      display: flex;
      justify-content: space-between;
      align-items: center;

      .title {
        font-size: 20px;
        font-weight: 1000;
      }
      .btns {
        // 视觉平衡：对齐文字高度，而非行高
        position: relative;
        top: 1px;

        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 3px;
      }
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

        :nth-child(2) {
          all: revert;  // 消除 Tailwind CSS 影响
        }
      }
    }
  }
}
</style>
