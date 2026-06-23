# 关于

数字桌搭 Deskset 是一款采用 Tauri 框架开发的开源桌面美化应用，通过将网页嵌入系统桌面，用户能在该网页上定制自己的个性化桌面。

::: tip 开发阶段提示
数字桌搭正处于早期开发阶段，为了避免数据损失，建议定期备份以下文件：`/config` 配置、`/themes` 主题和你连接的 Obsidian 仓库。
:::

## 架构设计

数字桌搭主要由前端 Deskset 和后端 DesksetBack 两部分组成：

- **Deskset**：由 Tauri 编写的主程序，拥有两个窗口
  - Desktop 桌面窗口：嵌入系统桌面的全屏窗口，显示桌面部件
  - Manager 管理窗口：管理部件/主题的增删改查
- **DesksetBack**：Deskset 的子程序，运行一个 FastAPI 服务器
  - 前端桌面部件通过 REST API 获取数据
  - （正在开发）工作流引擎，允许用户编写自动化脚本

## 关联项目

- [数字桌搭后端](https://github.com/Nostalgia-Season-Train/DesksetBack)：数字桌搭的数据中心和自动化引擎
- [数字桌搭笔记接口](https://github.com/Nostalgia-Season-Train/DesksetNoteAPI)：负责与后端通信的 Obsidian 插件

## 开源许可

基于 [AGPL-3.0](https://github.com/Nostalgia-Season-Train/Deskset/blob/main/LICENSE) 许可发布。

## 交流

QQ 群：770889923
