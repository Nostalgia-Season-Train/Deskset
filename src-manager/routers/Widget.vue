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
import { ref } from 'vue'

const isOpenDialog = ref(false)
const dialogTitle = ref<string>('')
const dialogOptions = ref<{
  name: string,
  type: string,
  key: string,
  value: any,
  change: Function
}[]>([])

const editWidget = async (id: string) => {
  const widget = activeWidgetMap.get(id)
  if (widget!.options == null)
    return
  dialogTitle.value = `编辑 ${widget!.title} 配置`
  dialogOptions.value = widget!.options.map(item => {
    const newItem = {
      ...item,
      value: widget!.model[item.key],
      change: () => desktop.setWidgetModel(id, { [item.key]: newItem.value })
    }
    return newItem
  })
  isOpenDialog.value = true
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
  ElButton,
  ElInput,
  ElSwitch,
  ElSelect,
  ElOption,
  ElDatePicker,
  ElColorPicker,
  ElScrollbar
} from 'element-plus'
import { X } from 'lucide-vue-next'

// Element Plus 翻译
import { config } from '#manager/global/config'
import { ElConfigProvider } from 'element-plus'
import zh_cn from 'element-plus/es/locale/lang/zh-cn'

const locale = config.language == 'zh-cn' ? zh_cn : undefined
</script>


<template>
<div class="container">

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
      <div
        class="flex justify-between items-center"
        v-for="option in dialogOptions"
      >
        <div>{{ option.name }}</div>
        <ElConfigProvider :locale="locale">
          <component
            v-if="option.type == 'Input'"
            :is="ElInput"
            v-model="option.value"
            @change="option.change()"
          />
        </ElConfigProvider>
        <ElConfigProvider :locale="locale">
          <component
            v-if="option.type == 'DateTimePicker'"
            :is="ElDatePicker"
            type="datetime"
            v-model="option.value"
            @change="option.change()"
          />
        </ElConfigProvider>
        <ElConfigProvider :locale="locale">
          <component
            v-if="option.type == 'ColorPicker'"
            :is="ElColorPicker"
            show-alpha
            v-model="option.value"
            @change="option.change()"
          />
        </ElConfigProvider>
        <ElConfigProvider :locale="locale">
          <component
            v-if="option.type == 'ArrayFilter'"
            :is="ElButton"
            @click="option.value.push({
              type: 'is',
              isInvert: false,
              frontmatterKey: '',
              compareValue: ''
            }); option.change()"
            style="padding: 0 6px;"
          >添加条件</component>
        </ElConfigProvider>
      </div>

      <!-- 彻 底 疯 狂 ! -->
      <div v-if="dialogOptions[dialogOptions.length - 1].type == 'ArrayFilter'">
        <ElScrollbar max-height="220"><!-- 暂不进行动态计算 -->
          <div class="flex">
            <span style="width: 120px;">属性名</span>
            <span style="width: 40px;">取反</span>
            <span style="width: 120px">条件</span>
            <span class="flex-1">比较值</span>
            <span>删除</span>
          </div>
          <div
            class="flex"
            v-for="(filter, index) in dialogOptions[dialogOptions.length - 1].value"
          >
            <ElInput
              style="width: 120px;"
              v-model="filter.frontmatterKey"
              placeholder="Frontmatter"
              @change="dialogOptions[dialogOptions.length - 1].change()"
            />
            <ElSwitch
              style="width: 40px;"
              v-model="filter.isInvert"
              @change="dialogOptions[dialogOptions.length - 1].change()"
            />
            <ElSelect v-model="filter.type" @change="dialogOptions[dialogOptions.length - 1].change()" style="width: 120px">
              <ElOption value="is" style="padding: 0 12px;"/>
              <ElOption value="startsWith" style="padding: 0 12px;"/>
              <ElOption value="endsWith" style="padding: 0 12px;"/>
              <ElOption value="isEmpty" style="padding: 0 12px;"/>
              <ElOption value="contains" style="padding: 0 12px;"/>
            </ElSelect>
            <ElInput
              class="flex-1"
              style="width: 0;"
              v-model="filter.compareValue"
              placeholder="Value"
              :disabled="filter.type == 'isEmpty'"
              @change="dialogOptions[dialogOptions.length - 1].change()"
            /><!-- width: 0; 抵消默认宽度 -->
            <ElButton
              style="width: 30px;"
              @click="
                dialogOptions[dialogOptions.length - 1].value.splice(index, 1);
                dialogOptions[dialogOptions.length - 1].change()
              "
            >
              <X style="width: 16px; height: 16px;"/>
            </ElButton>
          </div>
        </ElScrollbar>
      </div>
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

.container {
  width: 100%;
  height: 100%;
  padding: 0 10px 5px 10px;

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
