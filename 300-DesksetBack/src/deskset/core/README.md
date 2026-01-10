# 核心 core 包

这里是数字桌搭后端（后文简称桌设）所有模块使用的公共代码


## 日志 log 模块
日志文件存储在 logs 目录下，采用 utf-8 编码。日志级别定义见下：
- INFO     信息
- WARNING  警告
- ERROR    错误
- CRITICAL 崩溃


## 配置 config 模块
配置文件存储在 config 目录下，采用 yaml 格式和 utf-8 编码。区别于 feature 包中以 conf 开头的配置，deskset.core.config 导出的 config 核心配置需要重启程序才能生效


## 本地化 locale 模块
定义了 _t 函数，翻译其包裹的字符串，效果：_t('translate') = '翻译'


## 标准 standard 模块
桌设错误 DesksetError 是可以预测的问题，被抛出后通过 FastAPI 统一捕获并返回标准 JSON 响应
