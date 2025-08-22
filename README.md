<div align="center">
  <img src="./Deskset.png" width="160px"></img>

  # 数字桌搭 Deskset

  ![CI状态](https://img.shields.io/github/actions/workflow/status/Nostalgia-Season-Train/Deskset/auto-build.yaml)
  ![开源许可](https://img.shields.io/github/license/Nostalgia-Season-Train/Deskset)
  ![Star数量](https://img.shields.io/github/stars/Nostalgia-Season-Train/Deskset)

  <div>欢迎使用数字桌搭 Deskset</div>
  <div>一款桌面美化软件</div>
  <div>基于 Web 技术开发</div>
  <div>让桌面成为专属于你的高效工作台</div>
</div>

<br/>

<div align="center">
  <code>注意！数字桌搭正处于早期开发阶段，为了避免数据损失，建议定期备份重要文件</code>
</div>


## 简介
数字桌搭是一款采用 Tauri 框架开发的开源桌面美化应用，通过将网页嵌入系统桌面，用户能在该网页上定制自己的个性化桌面。软件内置时钟、秒表、倒计时、硬件监控、风格菜单等多个桌面美化部件。用户可以自由拖动，缩放，锁定这些部件，并将其位置，大小，属性保存进主题后分享给其他人。

### 效果展示
<img src="./2025-08-20.png" width="640px"/>


<!-- 用户手册 -->
## 快速开始

### 下载&运行
1、确认电脑装有 [WebView2](https://developer.microsoft.com/microsoft-edge/webview2) 运行库（Win11 及高版本 Win10 通常预装此库）<br/>
2、前往 [Releases](https://github.com/Nostalgia-Season-Train/Deskset/releases) 下载 Deskset.zip 压缩包<br/>
3、压缩包解压到独立文件夹，双击 Deskset.exe 即可运行数字桌搭


## 亮点
Tauri + FastAPI 前后端分离架构，通过嵌入桌面背景的网页显示桌面部件
- 部件：数字桌搭拥有多种增加学习和工作效率的部件，这些部件都能自由拖动、锁定和动态隐藏（仅在鼠标滑入时显示）<!-- 术语规范：严格使用 "部件 Widget" 而非 "组件 Component"，明确区分 Vue SFC 组件与桌面美化部件 -->
  - 在桌面上组织管理笔记，统计仓库数据
  - 实时监控设备的运行状态，可视化硬件资源
  - 自定义菜单栏，减少查找应用所需时间
  - 时钟日历，显示现在的时间日期
- 主题：支持部件布局的创建与共享，可以保存/应用主题模板


<!-- 开发指南 -->
## 开发你自己的部件 Widget 和插件 Plugin

### 部件开发
1、启动开发服务器：
- 通过命令行执行以下命令，启动 DesksetBack 服务器的开发模式
```cmd
DesksetBack.exe -dev -no-access
```

2、进入演练场
- 访问 http://127.0.0.1:6527/playground 进入数字桌搭演练场

3、创建部件
- 新建 my_widget 文件夹
- 新建 my_widget/main.vue 文件，复制粘贴演练场中的 Vue 代码
- 新建 my_widget/metainfo.json 文件，输入
```json
{
  "author": "作者",
  "version": "版本",
  "descript": "描述"
}
```

4、导入部件
- 打开 widgets 目录，若不存在则新建同名目录
- 复制你的部件 my_widget 文件夹到该目录内
- 运行 Deskset 添加 my_widget 部件，查看显示效果

### 插件开发
1、环境准备：
- 打开 plugins 目录，若不存在则新建同名目录
- 复制示例插件 sample_plugin 文件夹到该目录内

2、启动开发服务器：
- 通过命令行执行以下命令，启动 DesksetBack 服务器的开发模式
```cmd
DesksetBack.exe -dev -no-access
```

3、开发与测试
- 访问 http://127.0.0.1:6527/docs 查看交互式 API 文档，在此测试 REST API 接口
- 编辑 plugins/sample_plugin 中的代码。服务器自带热重载，自动监控文件变化，保存修改后无需重启程序即可生效


## 架构设计
数字桌搭主要由前端 Deskset 和后端 DesksetBack 两部分所组成：

Deskset：由 Tauri 编写的主程序，拥有两个窗口
- Desktop 桌面窗口：调用 setBottom.dll/SetParent 嵌入系统桌面的全屏窗口，显示桌面部件
- Manager 管理窗口：管理部件/主题的增删改查，配置 DesksetBack 工作流

DesksetBack：是 Deskset 的子程序，运行一个 FastAPI 服务器
- 前端桌面部件通过 axios 访问 DesksetBack REST API 获取数据
- （正在开发）工作流引擎，允许用户编写自己的自动化脚本


## 关联项目
[数字桌搭后端](https://github.com/Nostalgia-Season-Train/DesksetBack)：数字桌搭的数据中心和自动化引擎<br/>
[数字桌搭笔记接口](https://github.com/Nostalgia-Season-Train/DesksetNoteAPI)：负责与后端通信的 Obsidian 插件


## 交流
QQ 群：770889923
