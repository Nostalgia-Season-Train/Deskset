<script lang="ts" setup>
/* ==== 设置视图 ==== */
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  ElButton,
  ElCard,
  ElForm,
  ElFormItem,
  ElOption,
  ElRadio,
  ElRadioGroup,
  ElSelect,
  ElSwitch,
  ElTag,
} from 'element-plus'

const autoStart = ref(false)
const darkMode = ref(document.documentElement.classList.contains('dark'))
const language = ref<'zh' | 'en'>('zh')
const logLevel = ref<'error' | 'warn' | 'info' | 'debug'>('info')

watch(darkMode, (val) => {
  document.documentElement.classList.toggle('dark', val)
})

const logEntries = ref([
  { time: '10:30:12', level: 'info', msg: '应用启动' },
  { time: '10:30:15', level: 'info', msg: '加载配置文件 config.json' },
  { time: '10:31:02', level: 'warn', msg: '部件 datetime-clock 的描述为空' },
  { time: '10:32:48', level: 'error', msg: 'Obsidian 仓库连接失败：网络超时' },
])

const levelTagType: Record<string, 'primary' | 'success' | 'warning' | 'danger' | 'info'> = {
  error: 'danger',
  warn: 'warning',
  info: 'info',
  debug: 'primary',
}

function saveSettings() {
  ElMessage.success('设置已保存')
}
</script>

<template>
  <div class="settings-view">
    <!-- 基础设置 -->
    <el-card class="card" shadow="hover">
      <template #header>
        <span><span class="material-symbols-outlined">settings</span> 基础设置</span>
      </template>
      <el-form label-width="160px">
        <el-form-item label="开机启动">
          <el-switch v-model="autoStart" />
        </el-form-item>
        <el-form-item label="深色模式">
          <el-switch v-model="darkMode" />
        </el-form-item>
        <el-form-item label="语言切换">
          <el-radio-group v-model="language">
            <el-radio value="zh">中文</el-radio>
            <el-radio value="en">English</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="日志级别">
          <el-select v-model="logLevel" style="width: 200px">
            <el-option value="error" label="Error" />
            <el-option value="warn" label="Warning" />
            <el-option value="info" label="Info" />
            <el-option value="debug" label="Debug" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveSettings">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 日志 -->
    <el-card class="card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span><span class="material-symbols-outlined">article</span> 日志</span>
          <el-button size="small" plain>清空日志</el-button>
        </div>
      </template>
      <div class="log-list">
        <div v-for="(log, i) in logEntries" :key="i" class="log-item">
          <span class="log-time">{{ log.time }}</span>
          <el-tag :type="levelTagType[log.level]" size="small">{{ log.level }}</el-tag>
          <span class="log-msg">{{ log.msg }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.settings-view {
  padding: 16px;
}

.card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-list {
  max-height: 360px;
  overflow: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
}

.log-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: var(--el-text-color-secondary);
  min-width: 80px;
}

.log-msg {
  flex: 1;
}
</style>
