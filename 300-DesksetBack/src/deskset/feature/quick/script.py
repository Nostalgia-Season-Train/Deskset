from asyncer import asyncify
from runpy import run_path
from asyncio import iscoroutinefunction

SCRIPT_LIB = './scripts'

# 执行 工作路径/SCRIPT_LIB 下的脚本
async def execute_script(path: str):
    # 第一步：执行顶层代码 + 执行主函数 if __name__ == '__main__'
    module = await asyncify(run_path)(f'{SCRIPT_LIB}/{path}', run_name='__main__')

    # 第二步：执行异步主函数 async def main()
    if 'main' in module and iscoroutinefunction(module['main']):
        await module['main']()
