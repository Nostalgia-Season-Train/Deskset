<script lang="ts" setup>
import desktop from '#manager/global/page/desktop'

const refresh = async () => {
  console.log(await desktop.helloworld())
}
refresh()


/* === SFC 成员 === */
import {
  activeWidgetMap,
  activeWidgetOnSelect
} from '#manager/global'


/* === SFC 方法 === */
import { appendWidget } from '#manager/main/widget'

const removeWidget = async (id: string) => {
  await desktop.removeWidget(id)
  activeWidgetMap.delete(id)
  activeWidgetOnSelect.value = null
}

/* --- 编辑部件配置 --- */
  // - [ ] 重构：这就是彻头彻尾的屎山...
  // 问题 1：option.value 并不随 widget.model 变化，仅在初始化时赋值
  // 问题 2：缺乏输入验证
  // 问题 3：缺乏修改失败后的错误处理
import { ref, h } from 'vue'
import { ElMessageBox } from 'element-plus'
import Edit from './Widget/EditMenu.vue'

const isOpenDialog = ref(false)
const dialogTitle = ref<string>('')
const dialogOptions = ref<{
  name: string,
  type: string,
  // type != 'tab'
  key: string,
  // type == 'tab'：分层面板
  content?: {
    name: string,
    type: string,
    key: string
  }[],
  value: any,
  change: Function
}[]>([])

const editWidget = async (id: string) => {
  const widget = activeWidgetMap.get(id)
  // 交给编辑按钮判断即可，这样不用改两处
  // if (widget!.option == undefined)
  //   return
  ElMessageBox({
    title: `编辑 ${widget!.title} 配置`,
    showConfirmButton: false,
    message: () => h(Edit, { modelValue: widget as any }),  // 编辑按钮已判断 option != undefined
    callback: () => {}
  })
}

const locateWidget = async (id: string) => {
  await desktop.locateWidget(id)
}

const switchWidgetProp = async (id: string, prop: string, state: boolean) => {
  await desktop.switchWidgetProp(id, prop, state)

  // RightInfo 下的 v-model 由本函数切换
  const widget = activeWidgetMap.get(id)

  if (prop == 'drag-lock') widget!.isDragLock = state
  if (prop == 'disable-interact') widget!.isDisableInteract = state
  if (prop == 'auto-hide') widget!.isAutoHide = state
}

const selectActiveWidget = async (id: string) => {
  activeWidgetOnSelect.value = activeWidgetMap.get(id) ?? null
}


/* === 子组件 === */
import Menu from './Widget/Left1stMenu.vue'
import List from './Widget/Left2ndList.vue'
import Info from './Widget/RightInfo.vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from '#shadcn/components/ui/dialog'
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent
} from '#shadcn/components/ui/tabs'
import {
  ElInput,
  ElDatePicker,
  ElColorPicker,
  ElScrollbar
} from 'element-plus'

// Element Plus 翻译
import { config } from '#manager/global/config'
import { ElConfigProvider } from 'element-plus'
import zh_cn from 'element-plus/es/locale/lang/zh-cn'

const locale = config.language == 'zh-cn' ? zh_cn : undefined
</script>


<template>
<div class="container-widget">

  <div class="left">
    <Menu @select="appendWidget" class="menu"/>
    <List @select="selectActiveWidget" class="list"/>
  </div>

  <div class="right">
    <Info
      v-if="activeWidgetOnSelect"
      v-model="activeWidgetOnSelect"
      class="info"
      @remove="removeWidget"
      @edit="editWidget"
      @locate="locateWidget"
      @switchProp="switchWidgetProp"
    />
  </div>

  <!-- 配置编辑时覆盖背景，避免误操作（如删除部件） -->
  <Transition>
    <div
      class="
        fixed top-0 left-0
        w-screen h-screen bg-black/80
      "
      v-show="isOpenDialog"
      @click="isOpenDialog = false"
    ></div>
  </Transition>

  <!-- @openAutoFocus.prevent：禁用自动聚焦 -->
  <!-- :modal=false：让 Element Plus 选择器能被点击 -->
  <!-- @interact-outside.prevent：让 Element Plus 选择器确认后，DialogContent 不会直接关闭 -->
  <Dialog v-model:open="isOpenDialog" :modal="false">
    <DialogContent @openAutoFocus.prevent @interact-outside.prevent>
      <DialogHeader>
        <DialogTitle>{{ dialogTitle }}</DialogTitle>
        <DialogDescription></DialogDescription>
      </DialogHeader>
      <ElConfigProvider :locale="locale">

        <ElScrollbar v-if="dialogOptions[0].type != 'tab'" max-height="70vh"><!-- 暂不进行动态计算 -->
          <div v-for="option in dialogOptions">
            <!-- *** 输入框 *** -->
            <div v-if="option.type == 'Input'">
              <div class="flex justify-between items-center">
                <div>{{ option.name }}</div>
                <ElInput v-model="option.value" @change="option.change()"/>
              </div>
            </div>
            <!-- *** 日期时间选择器 *** -->
            <div v-if="option.type == 'DateTimePicker'">
              <div class="flex justify-between items-center">
                <div>{{ option.name }}</div>
                <ElDatePicker type="datetime" v-model="option.value" @change="option.change()"/>
              </div>
            </div>
            <!-- *** 颜色选择器 *** -->
            <div v-if="option.type == 'ColorPicker'">
              <div class="flex justify-between items-center">
                <div>{{ option.name }}</div>
                <ElColorPicker show-alpha v-model="option.value" @change="option.change()"/>
              </div>
            </div>
          </div>
        </ElScrollbar>

        <!-- 分层面板：将选项 option 按面板 tab 分层 -->
        <Tabs v-else :default-value="0">
          <TabsList>
            <!-- style 覆盖本文件 * { padding: 0; } 样式 -->
            <TabsTrigger v-for="(tab, index) in dialogOptions" :value="index" style="padding: 0 10px;">
              {{ tab.name }}
            </TabsTrigger>
          </TabsList>
          <TabsContent v-for="(tab, index) in dialogOptions" :value="index">
            <ElScrollbar height="60vh">
              <div v-for="option in tab!.content">
                <!-- *** 输入框 *** -->
                <div v-if="option.type == 'Input'">
                  <div class="flex justify-between items-center">
                    <div>{{ option.name }}</div>
                    <ElInput v-model="tab.value[option.key]" @change="tab.change()"/>
                  </div>
                </div>
                <!-- *** 数字输入框 *** -->
                <div v-if="option.type == 'InputNumber'">
                  <div class="flex justify-between items-center">
                    <div>{{ option.name }}</div>
                    <ElInput v-model="tab.value[option.key]" @change="
                      tab.value[option.key] = Number(tab.value[option.key]);
                      tab.change()
                    "/>
                  </div>
                </div>
                <!-- *** 颜色选择器 *** -->
                <div v-if="option.type == 'ColorPicker'">
                  <div class="flex justify-between items-center">
                    <div>{{ option.name }}</div>
                    <ElColorPicker show-alpha v-model="tab.value[option.key]" @change="tab.change()"/>
                  </div>
                </div>
              </div>
            </ElScrollbar>
          </TabsContent>
        </Tabs>

      </ElConfigProvider>
    </DialogContent>
  </Dialog>

</div>
</template>


<style lang="less" scoped>
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
  gap: 5px;

  .left {
    width: 25%;
    height: 100%;

    display: flex;
    flex-direction: column;
    gap: 5px;

    :nth-child(2) {
      flex: 1;
    }
  }
  .right {
    width: 75%;
    height: 100%;
  }
}
</style>
