<script lang="ts" setup>
import { ref, watch, toRaw } from 'vue'
import axios from 'axios'

const model = defineModel<{
  title: string,
  filterGroup: any
}>({ required: true })

// 列宽：ElTableV2.columns[n].width
// 行高：ElTableV2.row-height
const columns = [{
  dataKey: 'file.name',
  title: '名称',
  width: 300
}]
const data = ref<any[]>([])

const refresh = async () => {
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


/* ==== 子组件 ==== */
import { ElTableV2, ElAutoResizer } from 'element-plus'
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
}
</style>
