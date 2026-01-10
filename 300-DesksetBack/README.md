# 数字桌搭后端 DesksetBack

数字桌搭后端是数字桌搭数据处理的中心和自动化工作流的引擎，基于 FastAPI 框架开发，通过 PyStand 独立部署。

![CI状态](https://img.shields.io/github/actions/workflow/status/Nostalgia-Season-Train/DesksetBack/autobuild.yaml)
![开源许可](https://img.shields.io/github/license/Nostalgia-Season-Train/DesksetBack)
![Star数量](https://img.shields.io/github/stars/Nostalgia-Season-Train/DesksetBack)


## 启动方式
双击 DesksetBack.exe 即可运行


## 命令行参数
```sh
-dev            # 启用开发者模式
-no-access      # 跳过身份验证（仅限开发者模式使用）
-token=<token>  # 直接设置 Bearer token
```


## 开发指南

### 插件开发
1、环境准备：
- 创建 plugins 目录（若不存在）
- 将示例插件 sample_plugin 复制到该目录内

2、启动开发模式：
- 通过命令行执行
```cmd
DesksetBack.exe -dev -no-access
```

3、开发与测试
- 服务器运行时，访问 http://127.0.0.1:6527/docs 查看交互式 API 文档，可以在此测试接口
- 在 plugins/sample_plugin 中编辑代码
- 热重载机制：服务器会自动监控文件变化，保存修改后无需重启程序即可生效
