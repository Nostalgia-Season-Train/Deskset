<script lang="ts" setup>
const emit = defineEmits(['change'])

type Filter = {
  type: string
  isInvert: boolean
  propertyKey: string
  compareValue: string | number
}
type FilterGroup = {
  match: string,
  filters: Array<Filter | FilterGroup>
}

const filterGroup = defineModel<FilterGroup>({ required: true })

const querySearch = (queryString: string, cb: any) => {
  const results = [
    { value: 'file.fullname',  label: '文件名' },
    { value: 'file.basename',  label: '文件主名' },
    { value: 'file.extension', label: '文件扩展名' },
    { value: 'file.folder',    label: '文件父文件夹' },
    { value: 'file.path',      label: '文件路径' },
    { value: 'file.ctime',     label: '文件创建时间' },
    { value: 'file.mtime',     label: '文件修改时间' },
    { value: 'file.size',      label: '文件大小' }
  ].filter(item => item.value.includes(queryString))
  cb(results)
}

import {
  ElButton,
  ElInput,
  ElAutocomplete,
  ElSwitch,
  ElSelect,
  ElOption,
  ElDatePicker
} from 'element-plus'
import { X } from 'lucide-vue-next'
</script>


<template>
<div>
  <!-- 添加按钮 -->
  <div style="display: flex; align-items: center;">
    <ElButton
      @click="filterGroup.filters.push({
        type: 'is',
        isInvert: false,
        propertyKey: '',
        compareValue: ''
      }); emit('change')"
    >添加条件</ElButton>
    <ElButton
      @click="filterGroup.filters.push({
        match: 'all',
        filters: [{
          type: 'is',
          isInvert: false,
          propertyKey: '',
          compareValue: ''
        }]
      }); emit('change')"
    >添加条件组</ElButton>
    <ElSelect v-model="filterGroup.match" @change="emit('change')" style="width: 100px">
      <ElOption value="all" label="匹配全部"/>
      <ElOption value="any" label="匹配任意"/>
    </ElSelect>
  </div>
  <div class="flex">
    <span style="width: 120px;">属性名</span>
    <span style="width: 40px;">取反</span>
    <span style="width: 120px">条件</span>
    <span class="flex-1">比较值</span>
    <span>删除</span>
  </div>
  <!-- 过滤器 -->
  <div v-for="(filter, index) in filterGroup.filters">
    <div v-if="(filter as any)?.match == undefined" style="display: flex; align-items: center;">
      <ElAutocomplete
        style="width: 120px;"
        v-model="(filter as Filter).propertyKey"
        placeholder="Property"
        :fetch-suggestions="querySearch"
        @change="emit('change')"
      >
        <template #default="{ item }">
          <div style="min-width: 160px; display: flex; justify-content: space-between;">
            <span class="label">{{ item.label }}</span>
            <span class="value">{{ item.value }}</span>
          </div>
        </template>
      </ElAutocomplete>
      <ElSwitch
        style="width: 40px;"
        v-model="(filter as Filter).isInvert"
        @change="emit('change')"
      />
      <ElSelect
        v-if="
          // @ts-ignore
          filter.propertyKey == 'file.ctime' || filter.propertyKey == 'file.mtime' || filter.propertyKey == 'file.size'
        "
        v-model="(filter as Filter).type" @change="emit('change')" style="width: 120px"
      >
        <ElOption value="=" style="padding: 0 12px;"/>
        <ElOption value=">" style="padding: 0 12px;"/>
        <ElOption value="<" style="padding: 0 12px;"/>
        <ElOption value=">=" style="padding: 0 12px;"/>
        <ElOption value="<=" style="padding: 0 12px;"/>
      </ElSelect>
      <ElSelect v-else v-model="(filter as Filter).type" @change="emit('change')" style="width: 120px">
        <ElOption value="is" style="padding: 0 12px;"/>
        <ElOption value="startsWith" style="padding: 0 12px;"/>
        <ElOption value="endsWith" style="padding: 0 12px;"/>
        <ElOption value="isEmpty" style="padding: 0 12px;"/>
        <ElOption value="contains" style="padding: 0 12px;"/>
      </ElSelect>
      <ElDatePicker
        v-if="(filter as Filter).propertyKey == 'file.ctime' || (filter as Filter).propertyKey == 'file.mtime'"
        class="flex-1"
        type="datetime"
        value-format="x"
        v-model="(filter as Filter).compareValue"
        @change="emit('change')"
      /><!-- value-format="x" compareValue 数字时间戳 -->
      <ElInput
        v-else
        class="flex-1"
        style="width: 0;"
        v-model="(filter as Filter).compareValue"
        placeholder="Value"
        :disabled="(filter as Filter).type == 'isEmpty'"
        @change="emit('change')"
      /><!-- width: 0; 抵消默认宽度 -->
      <ElButton
        style="
          width: 28px; height: 28px; padding: 0;
          display: flex; justify-content: center; align-items: center;
        "
        @click="
          filterGroup.filters.splice(index, 1);
          emit('change')
        "
      >
        <X style="width: 16px; height: 16px;"/>
      </ElButton>
    </div>
    <div v-else class="ml-1 border border-gray-300">
      <NoteFilter
        v-model="filterGroup.filters[index] as FilterGroup"
        @change="() => {
          if ((filterGroup.filters[index] as FilterGroup).filters.length == 0)
            filterGroup.filters.splice(index, 1)
          emit('change')
        }"
      />
    </div>
  </div>
</div>
</template>


<style lang="less" scoped>
:deep(.el-autocomplete>.el-input) {
  width: 100%;
}
</style>
