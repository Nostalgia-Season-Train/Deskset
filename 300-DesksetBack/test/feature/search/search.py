# 查找动态库
import glob

everything_path = glob.glob('**/everything/EverythingMain.dll', recursive=True)[0]  # 用第零个


# 导入动态库
import ctypes

everything = ctypes.windll.LoadLibrary(everything_path)  # 绝对路径导入，否则会失败

everything.getResult.restype = ctypes.c_char_p  # 设置返回类型


# 使用动态库
everything.search(ctypes.c_char_p('测试'.encode('gbk')))  # 临时性解决方案
print()

result = everything.getResult(0)
print()

print(str(result.decode('gbk')))
