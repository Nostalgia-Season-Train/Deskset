<div align="center">
  <img src="./Deskset.png" width="160px"></img>

  # 数字桌搭 Deskset

  ![CI状态](https://img.shields.io/github/actions/workflow/status/Nostalgia-Season-Train/Deskset/auto-build.yaml)
  ![开源许可](https://img.shields.io/github/license/Nostalgia-Season-Train/Deskset)
  ![Star数量](https://img.shields.io/github/stars/Nostalgia-Season-Train/Deskset)

  <div>欢迎使用数字桌搭 Deskset</div>
  <div>一款桌面美化软件</div>
  <div>基于 Web 技术开发</div>
  <div>让桌面成为你组织和管理笔记的专属工作台</div>
</div>

<br/>

<div align="center">
  <code>注意！数字桌搭正处于早期开发阶段，为了避免数据损失，建议定期备份数字桌搭所绑定的笔记仓库</code>
</div>


## 简介
数字桌搭是一款专注整合笔记应用的桌面美化软件，旨在扩展笔记使用边界并集成自动化工作流，提升个人生产力。


## 使用教程
请按照以下步骤进行下载和配置
- 确保电脑拥有 [WebView2](https://developer.microsoft.com/microsoft-edge/webview2) 运行库
- 在 Obsidian 中安装 [DesksetNoteAPI](https://github.com/Nostalgia-Season-Train/DesksetNoteAPI) 和 [Dataview](https://github.com/blacksmithgu/obsidian-dataview) 插件
- 前往 [Releases](https://github.com/Nostalgia-Season-Train/Deskset/releases) 下载数字桌搭本体的压缩包，解压到独立目录
- 运行数字桌搭，进入设置页面后输入 DesksetNoteAPI 插件中的端口号、用户名和密码，即可绑定笔记仓库


## 亮点
Tauri + FastAPI 前后端分离架构，通过嵌入桌面背景的网页显示桌面部件
- 部件：数字桌搭拥有多种增加学习和工作效率的部件，这些部件都能自由拖动、锁定和动态隐藏（仅在鼠标滑入时显示）<!-- 术语规范：严格使用 "部件 Widget" 而非 "组件 Component"，明确区分 Vue SFC 组件与桌面美化部件 -->
  - 在桌面上组织管理笔记，统计仓库数据
  - 实时监控设备的运行状态，可视化硬件资源
  - 自定义菜单栏，减少查找应用所需时间
  - 时钟日历，显示现在的时间日期
- 主题：支持部件布局的创建与共享，可以保存/应用主题模板


## 关联项目
[数字桌搭后端](https://github.com/Nostalgia-Season-Train/DesksetBack)：数字桌搭的数据中心和自动化引擎<br/>
[数字桌搭笔记接口](https://github.com/Nostalgia-Season-Train/DesksetNoteAPI)：负责与后端通信的 Obsidian 插件


## 交流
QQ 群：770889923
