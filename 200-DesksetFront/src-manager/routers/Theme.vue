<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import { ref } from 'vue'

const searchText = ref('')


/* === 主题创建/删除/应用 === */
import { message, messageInput } from '#desksetui/Message'

const saveTheme = async () => {
  const name = await messageInput(_t('保存主题'), '', _t('在此输入主题名称'), _t('取消'), _t('确认'))
  if (name == null || name == '')
    return
  await store.saveTheme(name)
}

const deleteTheme = async (name: string) => {
  if (!await message(_t('删除主题'), _t(`是否删除 `) + name + _t(` 主题？`), _t('取消'), _t('确认'))) 
    return
  await store.deleteTheme(name)
}

const applyTheme = async (name: string) => {
  await store.applyTheme(name)
}


/* === 组件 === */
import {
  ElScrollbar,
  ElButton as Button,
  ElInput as Input
} from 'element-plus'


/* ==== [ ] 测试中 Pinia ==== */
import { useThemeStore } from '#manager/main/theme'

const store = useThemeStore()
</script>


<template>
<div class="container-theme">

  <div class="header h-[36px]">
    <Input v-model="searchText" :placeholder="_t('搜索')"/>
    <Button @click="saveTheme">{{ _t('保存') }}</Button>
  </div>

  <div class="themes-wrapper">
    <ElScrollbar>
      <div class="themes" v-for="theme in store.themes">
        <div class="theme">
          <div class="left">
            <span class="text-deskset-primary">{{ theme.name }}</span>
          </div>
          <div class="middle">
            <span class="text-deskset-primary">{{ theme.savetime }}</span>
          </div>
          <div class="right">
            <Button @click="deleteTheme(theme?.name)">{{ _t('删除') }}</Button>
            <Button @click="applyTheme(theme?.name)">{{ _t('应用') }}</Button>
          </div>
        </div>
      </div>
    </ElScrollbar>
  </div>

  <div class="prompt" v-if="store.themes.length == 0"><!-- 可选链访问：themes 挂载后赋值 -->
    <div>
      <div class="text text-deskset-primary">{{ _t('暂无可用主题') }}</div>
      <div class="text text-deskset-primary">{{ _t('点击右上角按钮保存主题') }}</div>
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.container-theme {
  padding: 0 10px;

  // themes-wrapper 高度自适应
    // 注：标准盒子模型下，margin 和 padding 上的 height 应为 0
  height: 100%;
  display: flex;
  flex-direction: column;
  .themes-wrapper {
    overflow: hidden;
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

.prompt {
  width: 100%;
  height: calc(100% - 35px - 36px);  // 减去 menu 和 theme.header 高度，让文本以窗口高度 100vh 居中，保持视觉平衡

  display: flex;
  justify-content: center;
  align-items: center;

  color: #FFF;

  .text {
    text-align: center;
  }
}
</style>
