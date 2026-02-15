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
  <div>
    <div>笔记数</div>
    <div>{{ noteNum }}</div>
  </div>
  <div>
    <div>附件数</div>
    <div>{{ attachmentNum }}</div>
  </div>
  <div>
    <div>累计天</div>
    <div>{{ usedayNum }}</div>
  </div>
</div>
</template>


<style lang="less" scoped>
.vault-stats {
  box-sizing: border-box;
  width: 270px;
  height: 100px;

  color: #000;
  background: #FFF7;
  border: solid 1px #FFF;

  display: flex;
  justify-content: space-evenly;

  :nth-child(n) {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    :nth-child(1) {
      font-size: 22px;
    }
    :nth-child(2) {
      font-size: 20px;
      font-weight: 1000;
    }
  }
}
</style>
