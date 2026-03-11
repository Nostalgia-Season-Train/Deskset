<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

const activeFile = ref('')
const lastActiveFile = ref('')

const noteNum = ref(0)
const assertNum = ref(0)
const usedayNum = ref(0)
const noteTodayNum = ref(0)
const assetTodayNum = ref(0)
const vaultName = ref('')

const refreshActiveFile = async () => {
  const activeFilepath = (await axios.get('/v0/note/obsidian/common/active-file')).data.result as string ?? ''
  const activeFileTmp = activeFilepath.split('/').pop() ?? ''
  if (activeFile.value === activeFileTmp)
    return
  lastActiveFile.value = activeFile.value
  activeFile.value = activeFileTmp
}
refreshActiveFile()

const refresh = async () => {
  const vaultStatus = (await axios.get('/v0/note/obsidian/stats/vault_status')).data.result
  noteNum.value = vaultStatus.note_num
  assertNum.value = vaultStatus.asset_num
  usedayNum.value = vaultStatus.useday_num
  noteTodayNum.value = vaultStatus.note_today_num
  assetTodayNum.value = vaultStatus.asset_today_num
  const vaultMetainfo = (await axios.get('/v0/note/obsidian/common/metainfo')).data.result
  vaultName.value = vaultMetainfo?.rootpath.split('/').pop()
}
refresh()

const openObsidian = async () => {
  await axios.get('/v0/note/obsidian/winpage/open')
}


/* ==== 轮询 ==== */
import { useInterval } from 'vue-hooks-plus'

useInterval(refreshActiveFile, 5 * 1000)
useInterval(refresh, 5 * 60 * 1000)


/* ==== 子组件 ==== */
import {
  Book,
  FileDigit
} from 'lucide-vue-next'
</script>


<template>
<div class="vault-stats">

  <div class="first">
    <div class="icon"></div><!-- 连接显示蓝球，未连接显示红球 -->
    <div class="str">{{ vaultName }}</div><!-- 仓库名称（仓库父文件夹） -->
    <div class="str">ONLINE</div><!-- 装饰 -->
  </div>

  <div class="second">
    <div class="title">当前标签页</div>
    <div class="content">
      <div class="name"><!-- 仓库当前标签页 -->
        <div class="base">{{ activeFile }}</div>
      </div>
      <div class="type">
        <!-- 文件类型：.md 笔记 | 其他后缀 附件 -->
        <Book v-if="activeFile.endsWith('.md')"/>
        <FileDigit v-else/>
      </div>
    </div>
    <div class="latest-page">{{ lastActiveFile }}</div><!-- 上一个打开的页面，主名即可 -->
  </div>

  <div class="third">
    <div class="note-num">
      <div><Book/>笔记总数</div>
      <div>{{ noteNum }}<span class="today" v-show="noteTodayNum">+{{ noteTodayNum }}</span></div><!-- +5 代表今天创建了 5 篇笔记 -->
    </div>
    <div class="attach-num">
      <div><FileDigit/>附件总数</div>
      <div>{{ assertNum }}<span class="today" v-show="assetTodayNum">+{{ assetTodayNum }}</span></div>
    </div>
  </div>

  <div class="fourth">
    你已使用 Obsidian <span class="useday-num">{{ usedayNum }}</span> 天
  </div>

  <!-- 打开 Obsidian 仓库：跳转 Obsidian 窗口的口语化表述 -->
  <div class="fifth" @click="openObsidian">
    打开 Obsidian 仓库
  </div>

</div>
</template>


<style lang="less" scoped>
@import '../style.less';

* {
  font-family: 'MiSansVF';
  font-weight: 500;
}

.vault-stats {
  box-sizing: border-box;
  width: 280px;
  height: fit-content;

  .dsw-box();

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
      background: #29B6F6;
      border-radius: 50%;
    }
    .str:nth-child(2) {
      .dsw-text-title();
    }
    .str:nth-child(3) {
      margin-left: auto;
      padding: 3px 6px;
      .dsw-text();
      font-size: 10px;
      font-weight: 500;
      background: #FFF;
    }
  }

  /* --- 当前标签页 --- */
  .second {
    .title {
      .dsw-text();
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      .name {
        display: flex;
        align-items: flex-end;
        .base {
          .dsw-text-title();
        }
        // .ext {
        //   color: #1119;
        //   font-size: 16px;
        //   font-weight: 500;
        // }
      }
      .type {
        padding: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #FF9800;
        background: #FFECB3;
        svg {
          width: 20px;
          height: 20px;
          stroke-width: 2.5;
        }
      }
    }
    .latest-page {
      .dsw-text();
      font-size: 14px;
    }
  }

  /* --- 笔记总数、附件总数 --- */
  .third {
    display: flex;
    justify-content: space-between;
    gap: 7px;
    &>:nth-child(n) {
      padding: 5px;
      flex: 1;
      background: hsl(200, 10%, 96%);
      &>:first-child {
        display: flex;
        align-items: center;
        gap: 3px;
        .dsw-text();
        svg {
          width: 18px;
          height: 18px;
          stroke-width: 2;
        }
      }
      &>:last-child {
        margin: 4px 2px;
        .dsw-text-title();
        .today {
          color: #AED581;
          font-feature-settings: 'sups';
        }
      }
    }
  }

  /* --- 使用天数 --- */
  .fourth {
    .dsw-text();
    .useday-num {
      .dsw-text-title();
      font-feature-settings: 'tnum';  // 小米字体官网 thum 参数是错的
    }
  }

  /* --- 打开 Obsidian 仓库 --- */
  .fifth {
    padding: 3px;
    display: flex;
    justify-content: center;
    align-items: center;
    .dsw-text();
    color: #FFF;
    background: #7E57C2;
    transition: .3s;
    &:hover {
      background: #673AB7;
    }
    &:active {
      background: #9575CD;
    }
  }
}
</style>
