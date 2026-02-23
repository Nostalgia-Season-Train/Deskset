<script lang="ts" setup>
import { ref, watch, toRaw } from 'vue'
import axios from 'axios'
import { getIconData } from '@iconify/utils'
import { icons as fluentIcons } from '@iconify-json/fluent-emoji-flat'
import { icons as notoIcons } from '@iconify-json/noto'

const iconifyData = ref()

const model = defineModel<{
  /* --- 基础 --- */
  icon: string,
  title: string,

  /* --- 筛选 --- */
  filterGroup: any,

  /* --- 样式 --- */
  width: number,
  height: number,
  titleColor: string,
  numberColor: string,
  backgroundColor: string
}>({ required: true })

const number = ref(0)

const refresh = async () => {
  const filterGroup = toRaw(model.value.filterGroup)
  const rep = await axios.post('/v0/note/obsidian/stats/filter-frontmatter', filterGroup)
  number.value = rep.data.result.length
  const [set, name = ''] = model.value.icon.split(':')
  if (set === 'fluent-emoji-flat')
    iconifyData.value = getIconData(fluentIcons, name)
  if (set === 'noto')
    iconifyData.value = getIconData(notoIcons, name)
}
refresh()

watch(model.value, async () => await refresh())
</script>


<template>
<div class="note-stats">

  <div class="first">
    <!-- width、height、viewBox 保持 32 不要动，否则图标会偏移，用 CSS 调整大小 -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      :width="iconifyData?.width"
      :height="iconifyData?.height"
      :viewBox="`0 0 ${iconifyData?.width} ${iconifyData?.height}`"
      v-html="iconifyData?.body"
    ></svg>
    <span>{{ model.title }}</span>
  </div>

  <div class="second">
    {{ number }}
  </div>

</div>
</template>


<style lang="less" scoped>
* {
  font-family: 'MiSansVF';
}

.note-stats {
  box-sizing: border-box;
  width: 140px;
  height: fit-content;
  padding: 10px;

  background: #FFFD;
  border: solid 1px #FFF;  // 让子元素 margin 撑开 fit-content 高度而非溢出
  border-radius: 5px;
  box-shadow: 0 2px 4px #000A;

  .first {
    display: flex;
    align-items: center;
    gap: 5px;
    svg {
      padding: 4px;
      width: 20px;
      height: 20px;
      background: #FFF;
      border-radius: 5px;
    }
    span {
      position: relative;
      top: -1px;  // 视觉居中
      color: #333C;
      font-size: 18px;
      font-weight: 350;
    }
  }
  .second {
    margin: 5px 0px 0px 3px;
    color: #111;
    font-size: 20px;
    font-weight: 500;
    font-feature-settings: 'tnum';
  }
}
</style>
