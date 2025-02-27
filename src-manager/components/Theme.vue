<script setup>
import { DocumentAdd } from "@element-plus/icons-vue"

import desktop from './desktop'


// 保存主题
import { ElMessage, ElMessageBox } from 'element-plus'

const saveTheme = () => {
  ElMessageBox.prompt('请输入主题名称', {
    confirmButtonText: '保存',
    cancelButtonText: '取消',
    // inputPattern: ,
    // inputErrorMessage: '名称无效'
  })
  .then(({ value }) => {
    // 输入检查
    if (value == null || value == '') {
      throw new Error('名称不能为空')
    }

    // 通知桌面保存主题
    desktop.saveTheme(value)

    // 成功信息
    ElMessage({
      type: 'success',
      message: `主题 ${value} 保存成功`
    })

    // 1、保存需要时间，不要立即刷新
    // 2、刷新两次，间隔 0.5s 保证图片显示
    // 3、后面补上加载动画
    setTimeout(refreshThemeList, 100)
    setTimeout(refreshThemeList, 600)
  })
  .catch((error) => {
    if (error instanceof Error) {
      ElMessage({
        type: 'error',
        message: error.message
      })
    }
  })
}


// 刷新/获取主题
import { ref } from 'vue'

const themes = ref()

const refreshThemeList = async () => {
  themes.value = await window.electron.getAllThemes()
}
refreshThemeList()


// 使用主题
const useTheme = (themeName) => {
  if (themeName != undefined)
    desktop.useTheme(themeName)
}


// 删除主题
const deleteTheme = (themeName) => {
  if (themeName == undefined)
    return

  ElMessageBox.confirm(
    `是否删除 ${themeName} 主题？`,
    '删除主题',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    }
  )
  .then(() => {
    window.electron.deleteTheme(themeName)

    ElMessage({
      type: 'success',
      message: `主题 ${themeName} 删除成功`
    })

    setTimeout(refreshThemeList, 100)
  })
  .catch()
}
</script>


<template>
<el-scrollbar>

  <div class="theme-save">
    <el-card shadow="hover" @click="saveTheme">
      <div class="content">
        <span>保存主题</span>
        <el-icon size="20px"><DocumentAdd /></el-icon>
      </div>
    </el-card>
  </div>

  <div class="theme-container" v-for="theme in themes">
    <div class="left">
      <el-card shadow="never">
        <!-- 主题预览图：theme?.preview 路径格式：/theme/name/preview.png，否则可能无法预览 -->
        <!-- 图片 URL 加入动态查询参数，强制浏览器刷新 -->
        <img :src="theme?.preview + '?t=' + new Date()"></img>
      </el-card>
    </div>
    <div class="right">
      <div class="word">
        <div class="name">
          <span><b>{{ theme?.name }}</b></span>
        </div>
        <div class="save-time">
          <span>保存日期：</span>
          <span>{{ theme?.data?.savetime }}</span>
        </div>
      </div>
      <div class="button">
        <el-button type="primary" plain @click="useTheme(theme?.name)">
          应用主题
        </el-button>
        <el-button type="primary" plain @click="deleteTheme(theme?.name)">
          删除主题
        </el-button>
      </div>
    </div>
  </div>

</el-scrollbar>
</template>


<style scoped>
/* 主题保存：保存按钮 */
.theme-save {
  margin: 5px 5px 0 5px;
}

.theme-save :deep(.el-card) {
  width: 240px;
  height: 135px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.theme-save .content {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 主题容器：显示保存的主题 */
.theme-container {
  margin: 5px;
  display: flex;
}

.theme-container>.left :deep(.el-card) {
  width: 240px;
  height: 135px;
}
.theme-container>.left :deep(.el-card>.el-card__body) {
  width: 240px;
  height: 135px;
  padding: 0;
}
.theme-container>.left :deep(.el-card) img {
  width: 240px;
  height: 135px;
  background-color: #9E9E9E;
}

.theme-container>.right {
  margin-left: 5px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.theme-container>.right>.word>.name {
  font-size: 16px;
}

.theme-container>.right>.word>.save-time {
  font-size: 14px;
  color: gray;
}

.theme-container>.right>.button {
  display: flex;
  justify-content: center;
}
</style>
