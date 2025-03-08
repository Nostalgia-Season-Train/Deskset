<script setup>
import { ref } from "vue"
import axios from "axios"

const activitys = ref()

const refresh = async () => {
  const response = await axios.get("http://127.0.0.1:8000/v0/diary/activity")
  activitys.value = response.data.data
}
refresh()
defineExpose({ refresh })


import { useIntervalFn } from "@vueuse/core"

useIntervalFn(refresh, 30000)
</script>


<template>
<el-timeline style="padding-left: 5px;">
  <el-timeline-item
    v-for="activity in activitys"
    :timestamp="activity.create"
    style="
      font-size: 16px;
      --el-text-color-primary: #FFFFFF;
      --el-text-color-secondary: rgba(255, 255, 255, 0.65);
  ">
    {{ activity.content }}
  </el-timeline-item>
</el-timeline>
</template>
