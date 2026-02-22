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
</script>


<template>
<div class="vault-stats">

  <div class="first">
    <div></div><!-- 连接显示绿球，未连接显示红球 -->
    <div>仓库名</div><!-- 仓库名称（仓库父文件夹） -->
  </div>

  <div class="second">
    <div>当前标签页</div><!-- 仓库当前标签页 -->
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
.vault-stats {
  box-sizing: border-box;
  width: 280px;
  height: 320px;

  background: hsl(200, 10%, 90%);
  border: solid 1px #FFF;
  border-radius: 5px;
}
</style>
