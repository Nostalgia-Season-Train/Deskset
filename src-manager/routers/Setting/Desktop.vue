<script lang="ts" setup>
/* 选择桌面 */
import { ref } from 'vue'
import { ElInput } from 'element-plus'
import { desktopManager } from '../../child'

const desktopName = ref(desktopManager.current())

const chooseDesktop = async (event: any) => {
  if (event.key != 'Enter') {
    return
  }
  desktopManager.choose(desktopName.value)
}

/* 刷新桌面 */
import { ElButton } from 'element-plus'
import desktop from '../desktop'

const refreshPage = async () => {
  desktop.refresh()
}
</script>


<template>
<div>
  <div class="option">
    <div class="left">
      <div class="name">选择桌面</div>
      <div class="description">输入桌面名称</div>
    </div>
    <div class="right">
      <el-input
        v-model="desktopName"
        @keydown="chooseDesktop"
        style="width: 180px;"
      />
    </div>
  </div>
  

  <div class="option">
    <div class="left">
      <div class="name">刷新</div>
      <div class="description">强制刷新桌面，相当于 F5</div>
    </div>
    <div class="right">
      <el-button type="primary" @click="refreshPage">
        <span>F5</span>
      </el-button>
    </div>
  </div>

</div>
</template>


<style lang="less" scoped>
.option {
  margin: 10px 10px 0 10px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  .left {
    .name {
      font-size: 16px;
      color: black;
    }
    .description {
      font-size: 14px;
      color: gray;
    }
  }
}
</style>
