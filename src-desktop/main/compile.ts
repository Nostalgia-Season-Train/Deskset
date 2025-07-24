import { readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import { error as logError } from '@tauri-apps/plugin-log'

import {
  parse as sfcParse,
  compileScript as sfcCompileScript,
  compileStyleAsync as sfcCompileStyleAsync
} from '@vue/compiler-sfc'
import { parse as acornParse } from 'acorn'
import MagicString from 'magic-string'


export const compile = async (id: string, name: string): Promise<{ js: string, css: string }> => {
  /* --- 0、读取 vue 文件 --- */
  const text = await readTextFile(`./widgets/${name}/main.vue`, { baseDir: BaseDirectory.Resource })

  /* --- 1、预处理 SFC 代码 --- */
  const { descriptor, errors } = sfcParse(text)

  if (errors.length > 0) {
    for (const error of errors) {
      logError(`${error.name}: ${error.message}`)
      if (error.stack)
        logError(error.stack)
    }
    throw Error(`widgets/${name}/main.vue compile failed`)
  }

  const scopeId = `data-v-${id}`  // 样式作用域 ID

  /* --- 2.1、生成组件 JS 代码：编译 JS --- */
    // 参考文章：https://vue-compiler.iamouyang.cn/guide/vue-to-js.html
  const scriptBlock = sfcCompileScript(descriptor, {
    id: scopeId,
    inlineTemplate: true,  // 内联创建 template 元素，不需要 compileTemplate 构建 _sfc_render 函数
    genDefaultAs: '_deskset_main'  // 编译成 const _deskset_main = {} 的形式
  })

  /* --- 2.2、生成组件 JS 代码：替换导入逻辑 --- */
    // 将 import XXX from 'module' 转换为 const XXX = $deskset_module
    // 参考文章：https://www.freecodecamp.org/chinese/news/loading-remote-components-in-vue/
    // 参考代码：https://github.com/woai3c/rollup-plugin-import-to-const/blob/main/index.ts
  const code = scriptBlock.content
  const magicString = new MagicString(code)
  const ast = acornParse(code, {
    ecmaVersion: 'latest',
    sourceType: 'module'
  })

  ast.body.forEach((node) => {
    if (node.type == 'ImportDeclaration') {
      const { source, specifiers, start, end } = node
      const { value } = source

      if (specifiers.length == 0)
        return

      const replaceValue = `$deskset_${value}`
      let requireStatement = ''

      if (specifiers.length == 1) {
        requireStatement = `const {${specifiers[0].local.name}} = ${replaceValue}`
      } else {
        requireStatement = `const { ${specifiers
          // @ts-ignore
          .map((specifier: { imported: { name: string }, local: { name: string } }) => {
            if (specifier.imported?.name == replaceValue)
              return ''
            if (specifier.local?.name)
              return specifier.imported?.name + ': ' + specifier.local.name
            return specifier.imported?.name
          })
          .filter(Boolean)
          .join(', ')} } = ${replaceValue}`
      }
      magicString.overwrite(start, end, requireStatement)
    }
  })

  /* --- 2.3、生成组件 JS 代码：手动拼接 scopeId --- */
  const jsCode = magicString.toString()
    + `\n _deskset_main.__scopeId = '${scopeId}'`
    + '\nexport default _deskset_main'

  /* --- 3、生成组件 CSS 代码 ---*/
  let cssCode = ''

  for (const style of descriptor.styles) {
    const styleBlock = await sfcCompileStyleAsync({
      filename: descriptor.filename,
      id: scopeId,
      scoped: true,  // 样式限制作用域 scopeId
      source: style.content
    })
    cssCode += styleBlock.code
  }

  /* --- 4、返回结果 --- */
  return {
    js: jsCode,
    css: cssCode
  }
}
