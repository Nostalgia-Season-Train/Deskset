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
  ElButton,
  ElInput,
  ElTable,
  ElTableColumn
} from 'element-plus'


/* ==== [ ] 测试中 Pinia ==== */
import { useThemeStore } from '#manager/main/theme'

const store = useThemeStore()
</script>


<template>
<div class="content">

  <div class="themes-header">
    <ElInput v-model="searchText" :placeholder="_t('搜索')"/>
    <ElButton @click="saveTheme">{{ _t('保存') }}</ElButton>
  </div>

  <div class="themes-wrapper" v-if="store.themes.length != 0">
    <ElTable :data="store.themes" style="width: 100%; height: 100%;">
      <ElTableColumn label="名称" prop="name" width="150" fixed="left"/>
      <ElTableColumn label="保存时间" prop="savetime"/>
      <ElTableColumn label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <ElButton @click="deleteTheme(row.name)">{{ _t('删除') }}</ElButton>
          <ElButton @click="applyTheme(row.name)">{{ _t('应用') }}</ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
  </div>

  <div class="themes-prompt" v-else><!-- 可选链访问：themes 挂载后赋值 -->
    <div>
      <div class="text text-deskset-primary">{{ _t('暂无可用主题') }}</div>
      <div class="text text-deskset-primary">{{ _t('点击右上角按钮保存主题') }}</div>
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.content {
  padding: 0 var(--content-padding);
  padding-bottom: var(--content-padding);
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--content-padding);

  // themes-wrapper 高度自适应
  .themes-wrapper {
    height: 100%;
    background: var(--bg);
    overflow: hidden;
  }
}

.themes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 5px;

  :nth-child(1) {
    flex: 1;
  }
}

.themes {
  .theme {
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

.themes-prompt {
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
