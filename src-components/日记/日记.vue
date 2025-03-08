<script setup>
import { ref } from "vue"
import { desksetReq } from '../request'


// 日记内容和日记动态
import str内容 from "./日记组成/内容.vue"

const refstr内容 = ref()


// 前端：刷新显示 + 后端：打开日记
import dayjs from "dayjs"

const date = ref(new Date())
const isHideChild = ref(false)

const refresh = async () => {
  const stand_date = dayjs(date.value).format("YYYYMMDD")
  const open = await desksetReq.get(`/v0/obsidian/diary/open/${ stand_date }`)

  // 刷新内容和动态显示
  refstr内容.value.refresh()

  // 只有日记存在时，才显示内容动态
  if (open.data.success) {
    isHideChild.value = true
  } else {
    isHideChild.value = false
  }
}
refresh()


// 按钮：用 Obsidian 打开日记，前一天和后一天
import { DArrowLeft, DArrowRight } from "@element-plus/icons-vue"

const obsidian = async () => {
  await desksetReq.get("/v0/obsidian/diary/open-in-obsidian")
}

const subOneDay = () => {
  const previousDate = new Date(date.value)
  previousDate.setDate(date.value.getDate() - 1)
  date.value = previousDate
  refresh()
}

const addOneDay = () => {
  const previousDate = new Date(date.value)
  previousDate.setDate(date.value.getDate() + 1)
  date.value = previousDate
  refresh()
}


// 刷新日历：哪里有日记
const diaryListInMonth = ref([])

const isDiaryExist = ({ dayjs }) => {
  return diaryListInMonth.value.includes(dayjs.format("YYYYMMDD"))
}

const refreshCalendar = async (value) => {
  const yearmonth = dayjs(value).format("YYYYMM")
  const response = await desksetReq.get(`/v0/obsidian/diary/list-a-month/${ yearmonth }`)
  let diaryList = []
  for (const diary of response.data.data) {
    diaryList.push(diary?.date)
  }
  diaryListInMonth.value = diaryList
}

const onfocus = () => {  // 单击输入框打开日历时，也得刷新日历
  refreshCalendar(date.value)
}
</script>


<template>
<div class="diary">
  <div class="select">
    <el-button @click="subOneDay">
      <el-icon size="16"><DArrowLeft /></el-icon>
    </el-button>
    <el-date-picker
      v-model="date"
      type="date"
      @change="refresh()"
      @panel-change="refreshCalendar"
      @focus="onfocus"
      popper-class="default deskset-datetimepicker"
    >
      <template #default="cell">
        <div class="cell">
          <span class="text">{{ cell.text }}</span>
          <span class="mark" v-if="isDiaryExist(cell)"></span>
        </div>
      </template>
    </el-date-picker>
    <el-button @click="addOneDay">
      <el-icon size="16"><DArrowRight /></el-icon>
    </el-button>
  </div>
    <str内容 ref="refstr内容" @dblclick="obsidian"/>
</div>
</template>


<style scoped>
.diary {
  width: 315px;
  display: flex; flex-direction: column;
  overflow-wrap: break-word
}

.diary>.select {
  display: flex;
  justify-content: center; align-items: center;
}

.cell>.mark {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--el-color-primary);

  position: absolute;
  bottom: 0px; left: 50%; transform: translateX(-50%);
}

:deep(.el-button), :deep(.el-input__wrapper), :deep(.el-input__prefix), :deep(.el-input__inner) {
  color: white;
  background-color: #FFFFFF01;
  border-style: none;
  box-shadow: none;  /* 小一点的白色边框 */
}

:global(.default.deskset-datetimepicker .el-date-picker__header-label) {
  /* 月份选择显示有误：0 ~ 11，暂时屏蔽 */
  pointer-events: none;
  user-select: none;
}
</style>
