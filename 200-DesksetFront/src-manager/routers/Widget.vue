<script lang="ts" setup>
import { useWidgetStore } from '#manager/main/widget'

const store = useWidgetStore()


/* ==== 编辑部件配置 ==== */
// 避免在 store 里导入 Edit，保证导入次序
import { h } from 'vue'
import { ElMessageBox } from 'element-plus'
import Edit from './Widget/EditMenu.vue'

const editWidget = async (_: string) => {
  if (store.widgetOnSelect === null) return
  // 交给编辑按钮判断即可，这样不用改两处
  // if (widget!.option == undefined)
  //   return
  ElMessageBox({
    title: `编辑 ${store.widgetOnSelect!.title} 配置`,
    showConfirmButton: false,
    message: () => h(Edit, { modelValue: store.widgetOnSelect as any }),  // 编辑按钮已判断 option != undefined
    callback: () => { }
  })
}


/* ==== 子组件 ==== */
import Menu from './Widget/Left1stMenu.vue'
import List from './Widget/Left2ndList.vue'
import Clear from './Widget/Left3rdClear.vue'
import Info from './Widget/RightInfo.vue'
</script>


<template>
<div class="container-widget">

  <div class="left">
    <Menu @select="store.appendWidget" class="menu"/>
    <List :widgets="store.widgets" @select="store.selectWidget" class="list"/>
    <Clear @clear="store.clearWidgetList" class="clear"/>
  </div>

  <div class="right">
    <Info
      v-model="store.widgetOnSelect"
      class="info"
      @remove="store.removeWidget"
      @edit="editWidget"
      @locate="store.locateWidget"
    />
  </div>

</div>
</template>


<style lang="less" scoped>
@import '#manager/style.less';

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* --- Transition --- */
.v-enter-active,
.v-leave-active {
  transition: opacity .15s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}

/* --- Element Plus --- */
:deep(.el-input) {
  width: 185px;  // 缩小输入框宽度，让选择器在左侧显示
}

.container-widget {
  width: 100%;
  height: 100%;
  padding: var(--content-padding);
  padding-top: 0;

  display: flex;
  justify-content: space-between;
  gap: var(--content-padding);

  .left {
    padding: 5px;
    width: 25%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    .deskset-layer-first();
    .menu,.clear {
      height: 24px;
    }
    :nth-child(2) {
      flex: 1;
    }
  }
  .right {
    width: 75%;
    height: 100%;
    .deskset-layer-first();
  }
}
</style>
