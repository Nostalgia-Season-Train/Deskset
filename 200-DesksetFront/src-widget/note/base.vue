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
  title: string,
  filterGroup: any,
  noteProperty: any
}>({ required: true })

// 列宽：ElTableV2.columns[n].width
// 行高：ElTableV2.row-height
const columns = ref([])
const data = ref<any[]>([])

const refresh = async () => {
  columns.value = structuredClone(toRaw(model.value.noteProperty.props)).map((item: any) => {
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
          style: 'position: absolute; right: 0; width: 2px; height: 100%; background: var(--el-table-header-text-color); cursor: ew-resize;',
          onMousedown: (event) => down(event, event.target as HTMLElement, dataKey)
        })
      ])
    }
    return item
  })

  const filterGroup = toRaw(model.value.filterGroup)
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


/* ==== 拖动改变列宽 ==== */
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
    const modelItem: any = model.value.noteProperty.props.find((item: any) => item.dataKey == dataKey) || null
    if (item != null && modelItem != null) {
      item.width = item.width + moveX            // ElTableV2 列宽
      modelItem.width = modelItem.width + moveX  // 数据库配置 列宽
    }
  }
}
</script>


<template>
<div class="database">
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
</div>
</template>


<style lang="less" scoped>
.database {
  width: 540px;
  height: 250px;

  :deep(.el-empty) {
    padding: 0;
  }
  // 让分割线拖出所在格后仍显示
  :deep(.el-table-v2__header-cell) {
    overflow: visible;
  }
}
</style>
