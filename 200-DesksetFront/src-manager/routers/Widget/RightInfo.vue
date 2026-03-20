<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import { RuntimeWidget } from '#manager/main/widget'
import { prefixMark } from '#widget/register'

const widget = defineModel<RuntimeWidget | null>({ required: true })  // - [ ] 实际上不是 RuntimeWidget 类型，单纯方便编辑器智能提示


/* === 事件 === */
const emit = defineEmits([
  'remove',
  'edit',
  'locate',
  'switchProp'
])


/* ==== 子组件 ==== */
import {
  ElButton as Button,
  ElSwitch as Switch,
  ElInput as Input,
  ElSlider
} from 'element-plus'
</script>


<template>
<div class="rightinfo">

  <div class="top">
    <div class="first-line">
      <Input
        class="title"
        v-model="widget.title"
        v-if="widget"
      />
      <div
        class="title"
        v-else
      >...</div>
      <div class="btns">
        <div class="btn"><Button @click="emit('remove', widget?.id)" :disabled="widget == null">{{ _t('删除') }}</Button></div>
        <div class="btn"><Button @click="emit('edit', widget?.id)" :disabled="widget?.option == undefined">{{ _t('编辑') }}</Button></div>
        <div class="btn"><Button @click="emit('locate', widget?.id)" :disabled="widget == null">{{ _t('定位') }}</Button></div>
      </div>
    </div>
    <div class="name">名称：{{ widget?.name.startsWith(prefixMark) ? _t(widget?.name.replace(prefixMark, '')) : widget?.name }}</div>
    <div class="author">作者：{{ widget?.author }}</div><!-- - [ ] 需要翻译 -->
    <div class="version">版本：{{ widget?.version }}</div><!-- - [ ] 需要翻译 -->
    <div class="descript">描述：{{ widget?.descript }}</div><!-- - [ ] 需要翻译 -->
  </div>

  <div class="bottom">
    <div class="left">
      <div class="left-title">位置 & 大小</div><!-- - [ ] 需要翻译 -->
      <div class="left-item">
        <span>{{ _t('坐标') }}</span>
        <Input v-model="widget.x" v-if="widget"/>
        <Input disabled v-else/>
        <Input v-model="widget.y" v-if="widget"/>
        <Input disabled v-else/>
      </div>
      <div class="left-item">
        <span>{{ _t('缩放') }}</span>
        <Input v-model="widget.scale" v-if="widget"/>
        <Input disabled v-else/>
      </div>
      <div class="left-item">
        <span>{{ _t('透明度') }}</span>
        <ElSlider v-model="widget.opacity" :min="0" :step="0.01" :max="1" v-if="widget"/>
        <ElSlider disabled v-else/>
      </div>
    </div>

    <div class="right">
      <div class="right-title">状态</div><!-- 别跟状态模式搞混了！这是 CSS 类名（也别跟面向对象类搞混...）控制的部件行为 -->
      <div class="right-item">
        <span>{{ _t('锁定拖动') }}</span>
        <Switch v-model="widget.isDragLock" v-if="widget"/>
        <Switch disabled v-else/>
      </div>
      <div class="right-item">
        <span>{{ _t('禁用交互') }}</span>
        <Switch v-model="widget.isDisableInteract" v-if="widget"/>
        <Switch disabled v-else/>
      </div>
      <div class="right-item">
        <span>{{ _t('自动隐藏') }}</span>
        <Switch v-model="widget.isAutoHide" v-if="widget"/>
        <Switch disabled v-else/>
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

  .top {
    padding: 5px;
    flex: 1;

    .first-line {
      height: 28px;

      display: flex;
      justify-content: space-between;
      align-items: center;

      :deep(.title) {
        .el-input__wrapper {
          padding: 0;
          background: transparent;
          .el-input__inner {
            font-size: 20px;
            font-weight: 560;
          }
          &:hover, &.is-focus {
            box-shadow: none;
          }
        }
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
    height: 30%;

    display: flex;
    justify-content: space-between;
    align-items: stretch;  // 让子元素填满高度

    &>:nth-child(n) {
      margin: 5px;
      padding: 4px 6px;
      border: solid 1px var(--deskset-text-sharp-color);
    }
    .left {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      .left-title {
        text-align: center;
      }
      .left-item {
        display: flex;
        gap: 2px;
        &>* { width: 33.3%; }
      }
      .left-item:nth-child(3) {
        &>:last-child { width: 66.6%; }
      }
      .left-item:nth-child(4) {
        &>:last-child { width: 66.6%; }
      }
    }
    .right {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      .right-title {
        text-align: center;
      }
      .right-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }
  }
}
</style>
