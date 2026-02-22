<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

const noteNum = ref(0)
const attachmentNum = ref(0)
const usedayNum = ref(0)

const refresh = async () => {
  const vaultStatus = (await axios.get('/v0/note/obsidian/stats/vault_status')).data.result
  noteNum.value = vaultStatus.note_num
  attachmentNum.value = vaultStatus.attach_num
  usedayNum.value = vaultStatus.useday_num
}
refresh()


/* ==== 轮询 ==== */
import { useInterval } from 'vue-hooks-plus'

useInterval(refresh, 5 * 60 * 1000)


/* ==== 子组件 ==== */
import { Book } from 'lucide-vue-next'
</script>


<template>
<div class="vault-stats">

  <div class="first">
    <div class="icon"></div><!-- 连接显示绿球，未连接显示红球 -->
    <div class="str">PARA By Link</div><!-- 仓库名称（仓库父文件夹） -->
    <div class="str">ONLINE</div><!-- 装饰 -->
  </div>

  <div class="second">
    <div class="title">当前标签页</div>
    <div class="content">
      <div class="name"><!-- 仓库当前标签页 -->
        <div class="base">ComfyUI笔记</div>
        <div class="ext">.md</div>
      </div>
      <div class="type">
        <Book/><!-- 文件类型：.md 笔记 | 其他后缀 附件 -->
      </div>
    </div>
    <div class="latest-page">上次打开：主页.md</div><!-- 上一个打开的页面，主名即可 -->
  </div>

  <div class="third">
    <div class="note-num">
      <div>笔记总数</div>
      <div>Num:笔记总数</div>
      <div>Num:今日创建的笔记数</div>
    </div>
    <div class="attach-num">
      <div>附件总数</div>
      <div>Num:附件总数</div>
      <div>Num:今日创建的附件数</div>
    </div>
    <div class="useday0num">
      <div>使用天数</div>
      <div>Num:仓库使用天数</div>
    </div>
  </div>

  <div class="fourth">
    <div class="tag-num">
      <div>标签总数</div>
      <div>Num:标签总数</div>
    </div>
    <div class="task-num">
      <div>任务总数</div>
      <div>Num:任务总数</div>
    </div>
  </div>

  <div class="fifth">
    <div>打开 Obsidian 窗口</div>
  </div>

</div>
</template>


<style lang="less" scoped>
* {
  font-family: 'MiSansVF';
}

.vault-stats {
  box-sizing: border-box;
  width: 280px;
  height: 320px;

  background: hsl(200, 10%, 90%);
  border: solid 1px #FFF;
  border-radius: 5px;

  &>:nth-child(n) {
    margin: 12px;
  }

  /* --- 仓库名 --- */
  .first {
    height: 24px;
    display: flex;
    align-items: center;
    gap: 7px;
    .icon {
      position: relative;
      top: 1px;
      width: 10px;
      height: 10px;
      background: #4CAF50;
      border-radius: 50%;
    }
    .str:nth-child(2) {
      color: hsla(200, 20%, 12%, 80%);
      font-size: 18px;
      font-weight: 500;
    }
    .str:nth-child(3) {
      margin-left: auto;
      padding: 3px 6px;
      color: #333A;
      font-size: 10px;
      font-weight: 500;
      background: #FFF;
      border-radius: 5px;
    }
  }

  /* --- 当前标签页 --- */
  .second {
    .title {
      color: hsla(200, 20%, 12%, 40%);
      font-size: 16px;
      font-weight: 500;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      .name {
        display: flex;
        align-items: flex-end;
        .base {
          color: #111;
          font-size: 24px;
          font-weight: 500;
        }
        .ext {
          color: #1119;
          font-size: 16px;
          font-weight: 500;
        }
      }
      .type {
        padding: 3px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #FF9800;
        background: #FFECB3;
        border-radius: 5px;
      }
    }
    .latest-page {
      color: hsla(200, 20%, 12%, 60%);
      font-size: 14px;
      font-weight: 500;
    }
  }
}
</style>
