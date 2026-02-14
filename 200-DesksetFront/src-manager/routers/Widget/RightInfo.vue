<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import { RuntimeWidget } from '#manager/global'
import { prefixMark } from '#widget/register'

const widget = defineModel<RuntimeWidget>({ required: true })


/* === 事件 === */
const emit = defineEmits([
  'remove',
  'edit',
  'locate',
  'switchProp'
])

const ensureTitle = async () => {
  if (widget.value.title == '') {
    widget.value.title = widget.value.name.startsWith(prefixMark) ? _t(widget.value.name.replace(prefixMark, '')) : widget.value.name
  }
}

// - [ ] 后续：回退上个值而非默认值
import desktop from '#manager/global/page/desktop'

const ensureAxisX = async () => {
  const x = Number(widget.value.x) > 0 ? Number(widget.value.x) : null
  const axis = await desktop.setWidgetAxis(widget.value.id, x, widget.value.y)
  widget.value.x = axis.x
  widget.value.y = axis.y
  // setWidgetAxis 不会触发事件链 drag.ts > DesktopSend > main.ts 更新 widget 位置（left、top）
  widget.value.left = axis.left
  widget.value.top = axis.top
}

const ensureAxisY = async () => {
  const y = Number(widget.value.y) > 0 ? Number(widget.value.y) : null
  const axis = await desktop.setWidgetAxis(widget.value.id, widget.value.x, y)
  widget.value.x = axis.x
  widget.value.y = axis.y
  widget.value.left = axis.left
  widget.value.top = axis.top
}

const ensureScale = async () => {
  widget.value.scale = Number(widget.value.scale) > 0 ? Number(widget.value.scale) : 1
  await desktop.setWidgetScale(widget.value.id, widget.value.scale)
}


/* ==== 子组件 ==== */
import {
  ElButton as Button,
  ElSwitch as Switch,
  ElInput as Input
} from 'element-plus'
</script>


<template>
<div class="rightinfo">

  <div class="top">
    <div class="first-line">
      <input
        class="title selection:bg-primary selection:text-primary-foreground"
        v-model="widget.title"
        @change="ensureTitle"
      ></input>
      <div class="btns">
        <div class="btn"><Button @click="emit('remove', widget.id)">{{ _t('删除') }}</Button></div>
        <div class="btn" v-if="widget.option != null"><Button @click="emit('edit', widget.id)">{{ _t('编辑') }}</Button></div>
        <div class="btn"><Button @click="emit('locate', widget.id)">{{ _t('定位') }}</Button></div>
      </div>
    </div>
    <div class="name">{{ widget.name.startsWith(prefixMark) ? _t(widget.name.replace(prefixMark, '')) : widget.name }}</div>
    <div class="author">作者：{{ widget.author }}</div><!-- - [ ] 需要翻译 -->
    <div class="version">版本：{{ widget.version }}</div><!-- - [ ] 需要翻译 -->
    <div class="descript">描述：{{ widget.descript }}</div><!-- - [ ] 需要翻译 -->
  </div>

  <div class="bottom">
    <div class="left">
      <div class="left-title">位置 & 大小</div><!-- - [ ] 需要翻译 -->
      <div class="left-item">
        <span>{{ _t('坐标') }}</span>
        <Input v-model="widget.x" @change="ensureAxisX"/>
        <Input v-model="widget.y" @change="ensureAxisY"/>
      </div>
      <div class="left-item">
        <span>{{ _t('缩放') }}</span>
        <Input v-model="widget.scale" @change="ensureScale"/>
      </div>
    </div>

    <div class="right">
      <div class="right-title">属性</div><!-- - [ ] 需要翻译 -->
      <div class="right-item">
        <span>{{ _t('锁定拖动') }}</span>
        <Switch v-model="widget.isDragLock" @click="emit('switchProp', widget.id, 'drag-lock', widget.isDragLock)"/>
      </div>
      <div class="right-item">
        <span>{{ _t('禁用交互') }}</span>
        <Switch v-model="widget.isDisableInteract" @click="emit('switchProp', widget.id, 'disable-interact', widget.isDisableInteract)"/>
      </div>
      <div class="right-item">
        <span>{{ _t('自动隐藏') }}</span>
        <Switch v-model="widget.isAutoHide" @click="emit('switchProp', widget.id, 'auto-hide', widget.isAutoHide)"/>
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
  gap: 5px;

  color: var(--color-deskset-primary);

  .top {
    flex: 1;
    background: var(--bg);

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
    height: 30%;

    display: flex;
    justify-content: space-between;
    align-items: stretch;  // 让子元素填满高度
    gap: 5px;

    .left {
      padding: 2px 4px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      background: var(--bg);
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
    }
    .right {
      padding: 2px 4px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      background: var(--bg);
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
