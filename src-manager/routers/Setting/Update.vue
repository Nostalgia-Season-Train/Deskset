<script lang="ts" setup>
/* === Element Plus === */
import { ElButton, ElIcon, ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'


/* === 配置 === */
import { confUpdate } from './config'
import { ElSwitch, ElSelect, ElOption } from 'element-plus'


/* === 获取软件更新 === */
import { Octokit } from 'octokit'
import { download } from '@tauri-apps/plugin-upload'

const octokit = new Octokit({
  // auth: import.meta.env.VITE_DESKSET_GITHUB_TOKEN  // 好像不需要 token
})

import { getVersion } from '@tauri-apps/api/app'
import semver from 'semver'  // 比较版本大小，遵循语义化版本
import { updateDeskset } from '../../child'

const getReleasesLatest = async () => {
  try {
    const rep = await octokit.request('GET /repos/{owner}/{repo}/releases/latest', {
      owner: 'Nostalgia-Season-Train',
      repo: 'Deskset'
    })
    const version = await getVersion()  // 当前版本，通过 tauri.conf.json 定义

    if (rep.data.name == null) {
      throw Error('无法获取最新版本')
    }

    if (semver.gt(rep.data.name, version)) {
      ElMessageBox.confirm(
        `检测到新版本 ${rep.data.name}，是否更新数字桌搭`,
        '更新确认', {
          confirmButtonText: '确认',
          cancelButtonText: '取消'
        }
      ).then(async () => {
        const download_url = rep.data.assets[0].browser_download_url
        await download(
          download_url,
          './Deskset.zip',
          ({ progress, total }) => console.log(progress, total)
        )
        await updateDeskset('Deskset.zip')
        ElMessage({
          type: 'success',
          message: `更新成功，请重启数字桌搭`
        })
      })
    } else {
      ElMessage({
        type: 'success',
        message: `当前已是最新版本`
      })
    }
  } catch (error) {
    ElMessage({
      type: 'error',
      message: `错误！${error}`
    })
  }
}


/* === 组件 === */
import Button from '#manager/components/Button.vue'
import Switch from '#manager/components/Switch.vue'
</script>


<template>
<div>
  <div class="option">
    <div class="left">
      <div class="name">软件更新</div>
      <div class="description">检查数字桌搭最新版本</div>
    </div>
    <div class="right">
      <Button @click="getReleasesLatest">
        <Refresh />
      </Button>
    </div>
  </div>
  <div class="option">
    <div class="left">
      <div class="name">自动更新</div>
      <div class="description">是否开启自动更新</div>
    </div>
    <div class="right">
      <Switch v-model="confUpdate.AutoUpdate"/>
    </div>
  </div>
  <!-- <div class="option">
    <div class="left">
      <div class="name">版本类型</div>
      <div class="description">选择更新的版本类型</div>
    </div>
    <div class="right">
      <el-select v-model="confUpdate.VersionType" style="width: 100px;">
        <el-option value="Stable" label="稳定版"/>
        <el-option value="Preview" label="预览版"/>
      </el-select>
    </div>
  </div> -->
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
      color: #FFF;
    }
    .description {
      font-size: 14px;
      color: #FFFA;
    }
  }
}
</style>
