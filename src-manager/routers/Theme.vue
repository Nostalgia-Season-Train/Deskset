<script lang="ts" setup>
import { ref } from 'vue'
import { getAllThemes as readThemes } from '#manager/tauri'

const themes = ref()
const searchText = ref('')

const refresh = async () => {
  themes.value = await readThemes()
}
refresh()


/* === 主题创建/删除/应用 === */
import { message, messageInput } from '#manager/components/Message'
import { deleteThemeDir } from '#manager/tauri'
import desktop from './desktop'  // - [ ] 后面拿 Promise 包装

const createSingleTheme = desktop.saveTheme
const deleteSingleTheme = deleteThemeDir
const applySingleTheme = desktop.useTheme

const createTheme = async () => {
  const name = await messageInput('保存主题', '', '在此输入主题名称')
  if (name == null)
    return

  await createSingleTheme(name)
  setTimeout(refresh, 100)
  setTimeout(refresh, 600)
}

const deleteTheme = async (name: string) => {
  if (!await message('删除主题', `是否删除 ${name} 主题？`))
    return

  await deleteSingleTheme(name)
  setTimeout(refresh, 100)
}

const applyTheme = async (name: string) => {
  await applySingleTheme(name)
}


/* === 组件 === */
import { ElScrollbar } from 'element-plus'
import Button from '#manager/components/Button.vue'
import Input from '#manager/components/Input.vue'
</script>


<template>
<div class="container">

  <div class="header">
    <Input v-model="searchText" placeholder="搜索"/>
    <Button @click="createTheme">保 存</Button>
  </div>

  <div class="themes-wrapper">
    <el-scrollbar>
      <div class="themes" v-for="theme in themes">
        <div class="theme" v-if="searchText == '' || theme.name.includes(searchText)">
          <div class="left">
            <span>{{ theme?.name }}</span>
          </div>
          <div class="middle">
            <span>{{ theme?.data?.savetime }}</span>
          </div>
          <div class="right">
            <Button @click="deleteTheme(theme?.name)">删 除</Button>
            <Button @click="applyTheme(theme?.name)">应 用</Button>
          </div>
        </div>
      </div>
    </el-scrollbar>
  </div>

</div>
</template>


<style lang="less" scoped>
.container {
  padding: 0 10px;

  // themes-wrapper 高度自适应
    // 注：标准盒子模型下，margin 和 padding 上的 height 应为 0
  height: 100%;
  display: flex;
  flex-direction: column;
  .themes-wrapper {
    overflow: hidden;
  }

  // 去掉 ElScrollbar 滚动条
  :deep(.el-scrollbar__thumb) {
    display: none;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 5px;

  :nth-child(1) {
    flex: 1;
  }
}

.themes {
  margin: 5px 0;

  .theme {
    // 预期行为：首个元素 margin-top 与 theme margin-top 部分重叠，不会出现 5px + 3px = 8px 的情况
    margin-top: 3px;

    display: flex;
    justify-content: space-between;
    align-items: center;

    color: #FFF;

    .right {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 5px;
    }
  }
}
</style>
