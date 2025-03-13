<script setup>
import { ElScrollbar, ElButton, ElIcon, ElInput } from 'element-plus'
import { Refresh, CopyDocument, Upload } from "@element-plus/icons-vue"


import desktop from './desktop.ts'

const refreshPage = () => {
  desktop.refresh()
}

const openDevTool = () => {
  desktop.openDevTool()
}


/* === 配置 === */
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getDesksetReq } from '../tauri.ts'

const conf_vault = ref('')

const get_conf_vault = async () => {
  const desksetReq = await getDesksetReq()
  const rep = await desksetReq.get('/v0/config/app-obsidian-vault')
  conf_vault.value = rep.data.data
}
get_conf_vault()

const set_conf_vault = async () => {
  const desksetReq = await getDesksetReq()
  const rep = await desksetReq.post(
    '/v0/config/app-obsidian-vault',
    { 'path': conf_vault.value }
  )

  if (rep.data.success) {
    ElMessage({
      type: 'success',
      message: '设置 Obsidian 仓库成功'
    })
  } else if (!rep.data.success && conf_vault.value == '') {
    ElMessage({
      message: '解绑 Obsidian 仓库'
    })
  } else {
    ElMessage({
      type: 'error',
      message: '设置 Obsidian 仓库失败'
    })
  }
}


/* === 子组件 === */
import Update from './Setting/Update.vue'
</script>


<template>
<el-scrollbar>

  <div class="option">
    <div class="word">
      <div class="name">Obsidian 仓库</div>
      <div class="description">设置数字桌搭绑定的 Obsidian 仓库</div>
    </div>
    <div class="input">
      <el-input
        v-model="conf_vault"
        @change="set_conf_vault"
        clearable
        style="width: 180px;"
        placeholder="仓库路径"
      />
    </div>
  </div>

  <div class="option">
    <div class="word">
      <div class="name">刷新</div>
      <div class="description">强制刷新桌面，相当于 F5</div>
    </div>
    <div class="icon">
      <el-button type="primary" @click="refreshPage">
        <span>F5</span>
      </el-button>
    </div>
  </div>

  <Update />

</el-scrollbar>
</template>


<style scoped>
.option {
  margin: 10px 10px 0 10px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.option>.word>.name {
  font-size: 16px;
  color: black;
}
.option>.word>.description {
  font-size: 14px;
  color: gray;
}
</style>
