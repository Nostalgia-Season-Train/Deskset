<script setup>
/* === 组件预览 === */
import { shallowRef, defineAsyncComponent } from "vue"
import { widgets, categorys } from "../../src-components/widget_register"

const widgetNow = shallowRef()
const widgetPreview = shallowRef()
const widgetModel = new Object  // 有些组件需要传入 v-model = new Object
if (widgets.length > 0) {
  widgetNow.value = widgets[0]
  widgetPreview.value = defineAsyncComponent(widgets[0].content)
}

// 选择组件，计算 id，找到相关组件并预览
const handleSelect = (key, keyPath) => {
  const id = keyPath[0] + key

  for (const widget of widgets) {
    if (widget.id == id) {
      widgetNow.value = widget
      widgetPreview.value = defineAsyncComponent(widget.content)
    }
  }

  // 选择一次，查询一次桌面上的组件信息
  desktop.getWidgetOnDesktop(id)
}


// 组件信息显示
import { onBeforeUnmount } from 'vue'

const pageManager = new BroadcastChannel('pageManager')

pageManager.onmessage = async (event) => {
  value显示.value = event.data.isDisplay
  for (const [num, widgetProp] of widgetProps.value.entries()) {
    if (event.data.class.includes(widgetProp.prop)) {
      widgetPropsIs.value[num] = true
    } else {
      widgetPropsIs.value[num] = false
    }
  }
}
onBeforeUnmount(() => { pageManager.onmessage = null })  // 解除绑定，否则重进页面后 onmessage 会执行两次以上
if (widgets.length > 0) {
  desktop.getWidgetOnDesktop(widgets[0].id)  // 每次进入页面，查询第一个桌面上的组件
}


/* === 组件控制 === */
import { ref } from 'vue'
import desktop from './desktop'

// 是否显示
const value显示 = ref(false)
const triggerDisplay = (id) => {
  desktop.switchDisplay(id, value显示.value)
  for (const [num, widgetProp] of widgetProps.value.entries()) {
    setTimeout(() => triggerProp(id, widgetProp.prop, widgetPropsIs.value[num]), 100)  // 加入延时，确保打开后再应用属性
  }
}

// 组件属性：按照 is 添加/移除属性 prop
const widgetProps = shallowRef([
  {name: '锁定拖动', prop: 'drag-lock'},
  {name: '禁用交互', prop: 'disable-interaction'},
  {name: '自动隐藏', prop: 'auto-hide'}
])
const widgetPropsIs = ref(Array(widgetProps.value.length).fill(false))  // 属性是否开启

const triggerProp = (id, prop, is) => {
  desktop.switchProp(id, prop, is)
}
</script>


<template>
<el-container v-if="widgets.length > 0"><!-- 有组件才显示组件菜单 -->

  <el-aside width="30%">
    <el-scrollbar>
      <el-menu
        :default-active="widgets[0].name"
        :default-openeds="[String(categorys.keys().next().value + '/')]"
        @select="handleSelect"
      >
        <el-sub-menu v-for="category in [...categorys.keys()]" :index="category + '/'">
          <template #title>
            <span>{{ category }}</span>
          </template>
          <el-menu-item v-for="widget in categorys.get(category)" :index="widget">
            <span>{{ widget }}</span><!-- widget 是 categorys 中的组件名 -->
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </el-aside>

  <el-main>
    <el-scrollbar>
      <div class="preview">
        <Suspense>
          <component :is="widgetPreview" v-model="widgetModel"/>
        </Suspense>
      </div>
      <!-- 就让 v-model 变化触发 el-switch 切换动画，当成特性 -->
      <div class="option">
        <div>打开组件</div>
        <el-switch
          v-model="value显示"
          @click="triggerDisplay(widgetNow.id)"
        />
      </div>
      <div v-for="(widgetProp, num) in widgetProps" class="option">
        <div>{{ widgetProp.name }}</div>
        <el-switch
          v-model="widgetPropsIs[num]"
          @click="triggerProp(widgetNow.id, widgetProp.prop, widgetPropsIs[num])"
        />
      </div>
    </el-scrollbar>
  </el-main>

</el-container>
</template>


<style scoped>
.el-container {
  width: 100%;
  height: 100%;
}

/* 去掉侧边栏滚动条和分界线 */
:deep(.el-scrollbar__thumb) {
  display: none;
}
.el-menu {
  border: 0;
}

.el-main {
  padding: 10px;
}
.preview {
  padding: 5px;
  pointer-events: none;
  background-color: #9E9E9E;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(155,155,155,0.25);
  border-radius: 3px;
}

.option {
  margin: 5px 5px 0 5px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 3px;
  padding-left: 5px;
  padding-right: 5px;
  border: 1px solid rgba(155,155,155,0.25);
  border-radius: 5px;
}
</style>
