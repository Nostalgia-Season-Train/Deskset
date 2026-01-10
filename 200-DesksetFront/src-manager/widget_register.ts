import { readDir, BaseDirectory } from '@tauri-apps/plugin-fs'


// 1、Resource 是 tauri.exe 所在目录，开发时在 src-tauri/target/debug
// 2、权限问题
  // - 检查拼写
  // - 检查路径，注意 $RESOURCE != $RESOURCE/*
const entrys = await readDir('', { baseDir: BaseDirectory.Resource })

console.log(entrys)
