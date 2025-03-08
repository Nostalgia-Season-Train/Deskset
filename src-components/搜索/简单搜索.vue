<script setup>
import { ref } from "vue"
import { Search } from "@element-plus/icons-vue"
import { desksetReq } from '../request'

const input = ref('')        // 输入框文字
const suggests = ref([])     // 搜索建议（结果）
const selectIndex = ref(-1)  // 被选中的搜索建议索引

/* 每次输入，都进行搜索并显示结果 */
const refresh = async (queryString) => {
  const rep = await desksetReq.get(`/v0/obsidian/search/find-note?query=${queryString}`)
  suggests.value = rep.data.data
}

/* choose_by_enter 在输入框按下键盘 Enter；choose_by_click 在搜索建议栏按下鼠标左键 */
const choose_by_enter = async () => {
  if (suggests.length == 0 || selectIndex.value == -1)
    return
  open(suggests.value[selectIndex.value])
}
const choose_by_click = async (relpath) => {
  if (suggests.length == 0)
    return
  open(relpath)
}

/* 在 Obsidian 中打开笔记 */
const open = async (relpath) => {
  desksetReq.get(`/v0/obsidian/search/open-note/${relpath}`)
  desksetReq.get(`/v0/obsidian/search/find-note`)  // 空查询，清空服务器缓存
  input.value = ''
  suggests.value = []
  selectIndex.value = -1
}

/* 键盘上下选择 */
const selectIndexAdd = async () => {
  const furtureIndex = selectIndex.value + 1
  if (furtureIndex < suggests.value.length)
    selectIndex.value = furtureIndex
}
const selectIndexSub = async () => {
  const furtureIndex = selectIndex.value - 1
  if (furtureIndex >= 0)
    selectIndex.value = furtureIndex
}
</script>


<template>
  <div class="search">
    <el-input v-model="input" :prefix-icon="Search" placeholder="搜索"
      style="width: 320px; height: 45px;"
      @input="refresh"
      @keydown.enter="choose_by_enter()"
      @keydown.down="selectIndexAdd"
      @keydown.up="selectIndexSub"
    />
    <el-scrollbar max-height="32vh">
    <div v-for="(suggest, index) in suggests"
      @click="choose_by_click(suggest)"
      @mouseenter="selectIndex = index"
      :class="['suggest', { select: selectIndex === index }]"
    >
      {{ suggest }}
    </div>
    </el-scrollbar>
  </div>
</template>


<style scoped>
/* 搜索框字体上下居中 */
:deep(.el-input__inner) {
  display: flex;
  align-items: center;
}

/* 搜索建议（自动填充）*/
.suggest {
  width: 320px;
  color: white;
  background-color: #FFFFFF01;
}
.suggest.select {
  background-color: rgba(224, 224, 224, 0.25)
}
</style>
