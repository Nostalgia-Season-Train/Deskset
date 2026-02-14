<!--
==== ==== ==== ====
已知问题：desktop.rs 原始输入转发不能反向设置鼠标光标样式 cursor: ew-resize;
==== ==== ==== ====
-->


<script lang="ts" setup>
import { ref, watch, toRaw, h } from 'vue'
import axios from 'axios'
import dayjs from 'dayjs'
import { ElTableV2, ElAutoResizer } from 'element-plus'

const model = defineModel<{
  width: number,
  height: number,
  noteFilter: any,
  noteProp: any
}>({ required: true })

// 列宽：ElTableV2.columns[n].width
// 行高：ElTableV2.row-height
const columns = ref([])
const data = ref<any[]>([])

const refresh = async () => {
  columns.value = structuredClone(toRaw(model.value.noteProp.props)).map((item: any) => {
    // 格式化时间
    if (item.dataKey == 'file.ctime' || item.dataKey == 'file.mtime') {
      item.cellRenderer = ({ cellData: date }: { cellData: number }) => {
        return h('div', dayjs(date).format('YYYY-MM-DD HH:mm:ss'))
      }
    }
    // 拖动分割线，改变列宽
    const title = item.title
    const dataKey = item.dataKey
    item.headerCellRenderer = () => {
      return h('div', { style: 'position: relative; width: 100%; height: 100%; display: flex;' }, [
        h('div', { style: 'display: flex; align-items: center;' }, title),
        h('div', {
          class: 'column-divider',
          style: `
            position: absolute; right: 0;
            width: 4px; height: ${model.value.height}px;
            background: transparent;
            cursor: ew-resize;
          `,
          onMousedown: (event) => down(event, event.target as HTMLElement, dataKey)
        })
      ])
    }
    return item
  })

  const filterGroup = toRaw(model.value.noteFilter)
  const rep = await axios.post('/v0/note/obsidian/stats/filter-frontmatter', filterGroup)
  data.value = rep.data.result
}
refresh()

watch(model.value, async () => await refresh())

const openInObsidian = async (event: any) => {
  const path = event.rowData['file.path']
  if (path != '')
    await axios.get(`/v0/note/obsidian/common/open-in-obsidian?path=${path}`)
}


/* ==== 拖动 ElTableV2列分割线 改变 ElTableV2列宽 ==== */
const down = (event: MouseEvent, element: HTMLElement, dataKey: string) => {
  // 阻止事件冒泡，避免触发整个组件的拖动行为（drag 函数）
  event.stopPropagation()
  // 保持指针样式不变
  document.body.style.cursor = 'ew-resize'
  // 保存拖动起始位置
  const originX = element.offsetLeft  // 元素起始位置
  const beginX = event.clientX        // 鼠标起始位置
  let moveX = 0  // 鼠标移动距离

  // 开始监听 mousemove、mouseup 事件
  document.onmousemove = (event: MouseEvent) => {
    moveX = event.clientX - beginX
    element.style.left = moveX + originX + 'px'
  }
  document.onmouseup = () => {
    // 停止监听
    document.onmousemove = null
    document.onmouseup = null
    // 还原指针样式默认
    document.body.style.cursor = 'default'
    // 设置拖动后列宽
    const item: any = columns.value.find((item: any) => item.dataKey == dataKey) || null
    const modelItem: any = model.value.noteProp.props.find((item: any) => item.dataKey == dataKey) || null
    if (item != null && modelItem != null) {
      item.width = item.width + moveX            // ElTableV2 列宽
      modelItem.width = modelItem.width + moveX  // 数据库配置 列宽
    }
  }
}


/* ==== 拖动 本组件边角 改变 本组件宽高 ==== */
const resize = (event: MouseEvent) => {
  const className = (event.target as HTMLElement).className  // 本组件被拖动边角的类名
  event.stopPropagation()
  if (className == 'right-border') { document.body.style.cursor = 'ew-resize' }
  if (className == 'bottom-border') { document.body.style.cursor = 'ns-resize' }
  if (className == 'right-bottom-corner') { document.body.style.cursor = 'nwse-resize' }
  const beginX = event.clientX
  const beginY = event.clientY
  const width = model.value.width    // model.value.width 直接加 moveX 是双倍变化
  const height = model.value.height  // 同上
  let moveX = 0
  let moveY = 0

  document.onmousemove = (event: MouseEvent) => {
    moveX = event.clientX - beginX
    moveY = event.clientY - beginY
    if (className == 'right-border') {
      model.value.width = width + moveX
    }
    if (className == 'bottom-border') {
      model.value.height = height + moveY
    }
    if (className == 'right-bottom-corner') {
      model.value.width = width + moveX
      model.value.height = height + moveY
    }
  }
  document.onmouseup = () => {
    document.onmousemove = null
    document.onmouseup = null
    document.body.style.cursor = 'default'
  }
}
</script>


<template>
<div class="database" :style="`width: ${model.width}px; height: ${model.height}px;`">
  <ElAutoResizer>
    <template #default="{ width, height }">
      <ElTableV2
        :columns="columns"
        :data="data"
        :width="width"
        :height="height"
        :header-height="40"
        :row-height="30"
        :row-event-handlers="{ onDblclick: openInObsidian }"
        fixed
      />
    </template>
  </ElAutoResizer>
  <div class="right-border" @mousedown="resize"></div>
  <div class="bottom-border" @mousedown="resize"></div>
  <div class="right-bottom-corner" @mousedown="resize"></div>
</div>
</template>


<style lang="less" scoped>
.database {
  position: relative;

  // ElTableV2样式
  :deep(.el-empty) {
    padding: 0;
  }
  // 让分割线拖出所在格后仍显示
  :deep(.el-table-v2__header-cell) {
    overflow: visible;
  }
  // 让分割线溢出表头
  :deep(.el-table-v2__header-wrapper) {
    overflow: visible;
    .el-table-v2__header {
      overflow: visible;
    }
  }
  // 显示分割线，从交互分割线内部向外发散阴影
  :deep(.column-divider::after) {
    content: '';
    position: absolute;
    left: -4px;
    width: 100%;
    height: 100%;
    box-shadow: 2px 0 4px #0002;
  }
  // 最右边的列分割线自动隐藏
  :deep(.el-table-v2__header-cell:last-child) {
    .column-divider {
      opacity: 0;
      transition: opacity .1s;
    }
    .column-divider:hover {
      opacity: 1;
    }
    .column-divider:active {
      opacity: 1;
    }
  }

  // 被拖动边角样式
  --len: 4px;  // 被拖动边角的长度（右边宽度，下边高度，右下角宽高）
  .right-border {
    position: absolute;
    top: 0px;
    right: calc(2px - var(--len));
    width: var(--len);
    height: 100%;
    background: transparent;
    cursor: ew-resize;
  }
  .bottom-border {
    position: absolute;
    bottom: calc(2px - var(--len));
    left: 0px;
    width: 100%;
    height: var(--len);
    background: transparent;
    cursor: ns-resize;
  }
  .right-bottom-corner {
    position: absolute;
    bottom: calc(2px - var(--len));
    right: calc(2px - var(--len));
    width: var(--len);
    height: var(--len);
    background: transparent;
    cursor: nwse-resize;
  }
}
</style>
