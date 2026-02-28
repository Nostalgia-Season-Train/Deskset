<script lang="ts" setup>
import { _t } from '#manager/main/i18n'
import { ref } from 'vue'

const searchText = ref('')


/* === 主题创建/删除/应用 === */
import { ElMessageBox } from 'element-plus'

const saveTheme = async () => {
  ElMessageBox.prompt(
    _t('请输入主题名称：'),
    _t('保存主题'), {
    cancelButtonText: _t('取消'),
    confirmButtonText: _t('确认'),
    callback: async (event: any) => {
      if (event.action == 'confirm') {
        const name = event.value
        if (name == undefined || name == null || name == '')
          return
        await store.saveTheme(name)
      }
    }
  })
}

const deleteTheme = async (name: string) => {
  ElMessageBox.confirm(
    _t(`是否删除 `) + name + _t(` 主题？`),
    _t('删除主题'), {
    cancelButtonText: _t('取消'),
    confirmButtonText: _t('确认'),
    callback: async (event: any) => {
      if (event == 'confirm') {
        await store.deleteTheme(name)
      }
    }
  })
}

const applyTheme = async (name: string) => {
  ElMessageBox.confirm(
    _t(`是否应用 `) + name + _t(` 主题？`),
    _t('应用主题'), {
    cancelButtonText: _t('取消'),
    confirmButtonText: _t('确认'),
    callback: async (event: any) => {
      if (event == 'confirm') {
        await store.applyTheme(name)
      }
    }
  })
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

  <div class="themes-wrapper">
    <ElTable
      empty-text="暂无可用主题，点击右上角按钮保存主题"
      :data="store.themes"
      style="width: 100%; height: 100%;"
    >
      <ElTableColumn label="名称" prop="name" width="200" fixed="left"/>
      <ElTableColumn label="保存时间" prop="savetime"/>
      <ElTableColumn label="操作" width="350" fixed="right">
        <template #header>
          <div
            style="width: 100%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 5px;
          ">
            <ElInput
              v-model="searchText"
              :placeholder="_t('搜索')"
              style="width: 150px;"
            />
            <ElButton @click="saveTheme">{{ _t('保存') }}</ElButton>
          </div>
        </template>
        <template #default="{ row }">
          <div
            style="width: 100%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 5px;
          ">
            <ElButton @click="deleteTheme(row.name)">{{ _t('删除') }}</ElButton>
            <ElButton @click="applyTheme(row.name)">{{ _t('应用') }}</ElButton>
          </div>
        </template>
      </ElTableColumn>
    </ElTable>
  </div>

</div>
</template>


<style lang="less" scoped>
@import '#manager/style.less';

.content {
  padding: 0 var(--content-padding);
  padding-bottom: var(--content-padding);
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--content-padding);

  // themes-wrapper 高度自适应
  .themes-wrapper {
    height: calc(100% - var(--content-padding));
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
    .deskset-text-title();
    text-align: center;
  }
}
</style>
