<script lang="ts" setup>
import { ref } from 'vue'
import { getAllThemes as readThemes } from '#manager/tauri'

const themes = ref()

const refresh = async () => {
  themes.value = await readThemes()
}
refresh()


/* === 组件 === */
import { ElScrollbar } from 'element-plus'
import Button from '#manager/components/Button.vue'
import Input from '#manager/components/Input.vue'
</script>


<template>
<div class="container">

  <div class="header">
    <Input/>
    <Button>保 存</Button>
  </div>

  <div class="themes-wrapper">
    <el-scrollbar>
      <div class="themes" v-for="theme in themes">
        <div class="theme" v-if="true"><!-- v-if 用于过滤搜索结果 -->
          <div class="left">
            <span>{{ theme?.name }}</span>
          </div>
          <div class="middle">
            <span>{{ theme?.data?.savetime }}</span>
          </div>
          <div class="right">
            <Button>删 除</Button>
            <Button>应 用</Button>
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
