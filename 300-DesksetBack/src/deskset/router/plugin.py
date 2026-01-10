# 模块导入顺序：core、feature、presenter => 外部插件 => router.plugin

# 获取插件
# 作用：遍历 ./plugins 目录，找出并返回插件（一个文件夹对应一个插件）
from pathlib import Path
from typing import TypedDict

class PluginType(TypedDict):
    name: str  # 插件名称：文件夹名称
    info: str  # 插件信息：register.yaml 相对路径
    init: str  # 插件入口： __init__.py  相对路径

def get_plugins() -> list[PluginType]:
    plugins: list[PluginType] = []

    for folder in Path('./plugins').glob('*'):
        if folder.is_dir():
            name = folder.name
            info = ''
            init = ''

            for file in Path(folder).glob('*.*'):
                if file.name == 'register.yaml':
                    info = str(file)
                if file.name == '__init__.py':
                    init = str(file)

            if info != '' and init != '':
                plugins.append({
                    'name': name,
                    'info': info,
                    'init': init
                })
            else:
                print(f'{name} 插件注册失败！')  # 稍后改成打印日志

    return plugins


# 直接从文件路径导入模块
import sys
import importlib.util
from types import ModuleType

def import_from_path(module_name: str, file_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# 注册插件
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token

router_plugin_root = APIRouter(prefix='/plugin', dependencies=[Depends(check_token)])  # 所有插件路由的根路径

for plugin in get_plugins():
    # 插件名称
    name = plugin['name']

    # 读取插件信息
    info = plugin['info']
    # with open(info, 'r', encoding='utf-8') as file:
    #     print(file.read())  # 待用

    # 包含插件路由
    init = plugin['init']

    url = '/' + name
    url_tags = ['Plugin: ' + name]
    router_plugin = APIRouter(prefix=url, tags=url_tags)

    module_name = 'deskset.plugin.' + name
    module = import_from_path(module_name, init)

    for attribute in dir(module):  # 遍历插件入口
        if not attribute.startswith('_'):  # 排除私有成员
            # 获取实际成员
            instance = getattr(module, attribute)

            if isinstance(instance, APIRouter) and getattr(instance, 'routes'):
                router_plugin.include_router(instance)

    if getattr(router_plugin, 'routes'):
        router_plugin_root.include_router(router_plugin)
    else:
        print(f'{name} 插件导入失败，未检查到任何路由路径！')  # 稍后改成打印日志
