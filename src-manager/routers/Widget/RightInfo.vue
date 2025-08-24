<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import { Widget } from '#manager/global'
import { prefixMark } from '#widget/register'

const widget = defineModel<Widget>({ required: true })


/* === 事件 === */
const emit = defineEmits([
  'remove',
  'edit',
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
}

const ensureAxisY = async () => {
  const y = Number(widget.value.y) > 0 ? Number(widget.value.y) : null
  const axis = await desktop.setWidgetAxis(widget.value.id, widget.value.x, y)
  widget.value.x = axis.x
  widget.value.y = axis.y
}

const ensureScale = async () => {
  widget.value.scale = Number(widget.value.scale) > 0 ? Number(widget.value.scale) : 1
  await desktop.setWidgetScale(widget.value.id, widget.value.scale)
}


/* === 子组件 === */
import Button from '#shadcn/components/ui/button/Button.vue'
import Switch from '#shadcn/components/ui/switch/Switch.vue'
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
        <div class="btn" v-if="widget.options != null"><Button @click="emit('edit', widget.id)">{{ _t('编辑') }}</Button></div>
        <div class="btn"><Button>{{ _t('定位') }}</Button></div>
      </div>
    </div>
    <div class="name">{{ widget.name.startsWith(prefixMark) ? _t(widget.name.replace(prefixMark, '')) : widget.name }}</div>
    <div class="author">作者：{{ widget.author }}</div><!-- - [ ] 需要翻译 -->
    <div class="version">版本：{{ widget.version }}</div><!-- - [ ] 需要翻译 -->
    <div class="descript">描述：{{ widget.descript }}</div><!-- - [ ] 需要翻译 -->
  </div>

  <div class="bottom">
    <div class="left">
      <div>
        <div class="text-center">位置 & 大小</div><!-- - [ ] 需要翻译 -->
        <div class="flex">
          <span class="w-1/3 text-center">{{ _t('坐标') }}</span>
          <input class="w-1/3 text-center" v-model="widget.x" @change="ensureAxisX"/>
          <input class="w-1/3 text-center" v-model="widget.y" @change="ensureAxisY"/>
        </div>
        <div class="flex">
          <span class="w-1/3 text-center">{{ _t('缩放') }}</span>
          <input class="w-2/3 text-center" v-model="widget.scale" @change="ensureScale"/>
        </div>
      </div>
    </div>

    <div class="right">
      <div class="text-center">属性</div><!-- - [ ] 需要翻译 -->
      <div class="option">
        <span>{{ _t('锁定拖动') }}</span>
        <Switch v-model="widget.isDragLock" @click="emit('switchProp', widget.id, 'drag-lock', !widget.isDragLock)"/>
      </div>
      <div class="option">
        <span>{{ _t('禁用交互') }}</span>
        <Switch v-model="widget.isDisableInteract" @click="emit('switchProp', widget.id, 'disable-interact', !widget.isDisableInteract)"/>
      </div>
      <div class="option">
        <span>{{ _t('自动隐藏') }}</span>
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

  color: var(--color-deskset-primary);

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
    height: 30%;

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
