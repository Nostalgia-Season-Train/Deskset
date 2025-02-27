<script setup>
import { Refresh, CopyDocument, Upload } from "@element-plus/icons-vue"


import desktop from './desktop'

const refreshPage = () => {
  desktop.refresh()
}

const openDevTool = () => {
  desktop.openDevTool()
}


/* === 配置 === */
import { ref } from 'vue'
import { desksetReq } from '../request'

const conf_vault = ref('')

const get_conf_vault = async () => {
  const rep = await desksetReq.get('/v0/config/app-obsidian-vault')
  conf_vault.value = rep.data.data
}
get_conf_vault()

const set_conf_vault = async () => {
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
        <el-icon style="margin: 0;"><Refresh /></el-icon>
      </el-button>
    </div>
  </div>

  <div class="option">
    <div class="word">
      <div class="name">开发工具</div>
      <div class="description">打开开发者工具</div>
    </div>
    <div class="icon">
      <el-button type="primary" @click="openDevTool">
        <el-icon style="margin: 0;"><CopyDocument /></el-icon>
      </el-button>
    </div>
  </div>

  <div class="option">
    <div class="word">
      <div class="name">导出日志</div>
      <div class="description">导出运行日志，以供调试</div>
    </div>
    <div class="icon">
      <el-button type="primary" @click="console.log('还未开发，按钮用来占位')">
        <el-icon style="margin: 0;"><Upload /></el-icon>
      </el-button>
    </div>
  </div>

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
