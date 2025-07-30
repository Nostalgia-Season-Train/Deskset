<script lang="ts" setup>
import { ref } from 'vue'
import { activeThemeMap } from '#manager/global'
import { activeWidgetMap, activeWidgetOnSelect } from '#manager/global'
import desktop from '#manager/global/page/desktop'

const searchText = ref('')


/* === 主题创建/删除/应用 === */
import dayjs from 'dayjs'
import { message, messageInput } from '#desksetui/Message'
import {
  saveTheme as saveThemeFile,
  deleteTheme as deleteThemeFile,
  readThemeData as readThemeDataFile
} from '#manager/main/theme'
import { convertWidgetInTheme } from '#manager/global'
import { getWidgetInfo } from '#manager/main/widget'

const saveTheme = async () => {
  const name = await messageInput('保存主题', '', '在此输入主题名称')
  if (name == null)
    return

  const data = (
    await Promise.all([...activeWidgetMap.values()].map(convertWidgetInTheme))
  ).filter(widget => widget != undefined)  // 转换失败的元素返回 undefined
  const info = {
    savetime: String(dayjs().format('YYYY-MM-DD HH:mm:ss')),
    descript: ''
  }

  await saveThemeFile(name, data, info)
  activeThemeMap.set(name, {
    name: name,
    savetime: info.savetime,
    descript: info.descript
  })
}

const deleteTheme = async (name: string) => {
  if (!await message('删除主题', `是否删除 ${name} 主题？`))
    return

  await deleteThemeFile(name)
  activeThemeMap.delete(name)
}

const applyTheme = async (name: string) => {
  const data = await readThemeDataFile(name)

  // 清空当前部件
  for (const widget of [...activeWidgetMap.values()]) {
    await desktop.removeWidget(widget.id)
  }
  activeWidgetMap.clear()
  activeWidgetOnSelect.value = null

  for (const widgetInThemeFile of data) {
    const widgetInTheme = await convertWidgetInTheme(widgetInThemeFile)
    if (widgetInTheme == undefined)
      return

    // 部件 ID
    let id = Math.random().toString(16).slice(2)
    for (let n = 0; n < 10; n++) {
      if (!activeWidgetMap.has(id))
        break
      id = Math.random().toString(16).slice(2)
    }

    // 部件信息（元数据）
    const widgetInfo = await getWidgetInfo(widgetInTheme.name)

    // 部件数据
    const widgetData = await desktop.appendWidget(
      id,
      widgetInTheme.name,
      widgetInTheme.isDragLock,
      widgetInTheme.isDisableInteract,
      widgetInTheme.isAutoHide,
      widgetInTheme.left,
      widgetInTheme.top
    )

    activeWidgetMap.set(id, {
      id: id,

      title: widgetInTheme.title,
      name: widgetInTheme.name,

      author: widgetInfo.author,
      version: widgetInfo.version,
      descript: widgetInfo.descript,

      isDragLock: widgetData.isDragLock,
      isDisableInteract: widgetData.isDisableInteract,
      isAutoHide: widgetData.isAutoHide,

      x: widgetData.x,
      y: widgetData.y,

      left: widgetData.left,
      top: widgetData.top
    })
  }
}


/* === 组件 === */
import ElScrollbar from '#element-plus/ElScrollbar.vue'
import Button from '#desksetui/Button.vue'
import Input from '#desksetui/Input.vue'
</script>


<template>
<div class="container">

  <div class="header">
    <Input v-model="searchText" placeholder="搜索"/>
    <Button @click="saveTheme">保 存</Button>
  </div>

  <div class="themes-wrapper">
    <ElScrollbar>
      <div class="themes" v-for="theme in Array.from(activeThemeMap.values())">
        <div class="theme" v-if="searchText == '' || theme.name.includes(searchText)">
          <div class="left">
            <span>{{ theme.name }}</span>
          </div>
          <div class="middle">
            <span>{{ theme.savetime }}</span>
          </div>
          <div class="right">
            <Button @click="deleteTheme(theme?.name)">删 除</Button>
            <Button @click="applyTheme(theme?.name)">应 用</Button>
          </div>
        </div>
      </div>
    </ElScrollbar>
  </div>

  <div class="prompt" v-if="activeThemeMap.size == 0"><!-- 可选链访问：themes 挂载后赋值 -->
    <div>
      <div class="text">暂无可用主题</div>
      <div class="text">点击右上角按钮保存主题</div>
    </div>
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
  height: calc(100% - 35px - 28px);  // 减去 menu 和 theme.header 高度，让文本以窗口高度 100vh 居中，保持视觉平衡

  display: flex;
  justify-content: center;
  align-items: center;

  color: #FFF;

  .text {
    text-align: center;
  }
}
</style>
