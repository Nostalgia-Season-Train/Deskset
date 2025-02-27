<script setup>
const openBrowser = (url) => {
  window.electron.openBrowser(url)
}
</script>


<template>
  <div style="padding: 5px;">
    数字桌搭支持通过 RESTful API 交互软件，以下是支持列表：
  </div>
  <div class="show">
    <div>
      <img src="/static/icons/obsidian.svg" height="50px"/>
      <a @click.prevent="openBrowser('https://obsidian.md')" href="">Obsidian</a>
    </div>
    <div>
      <img src="/static/icons/vscode.svg" height="50px"/>
      <a @click.prevent="openBrowser('https://code.visualstudio.com')" href="">Visual Studio Code</a>
    </div>
  </div>
</template>


<style scoped>
.show {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 10px;
  padding-top: 5px;
}

.show>div {
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  border: 1px solid #AAA;
  padding: 10px;
}
</style>
