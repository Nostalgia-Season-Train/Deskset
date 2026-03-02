// 代码功能：移除 element-plus-x 污染的 element-plus 样式
// 代码来源：https://github.com/element-plus-x/Element-Plus-X/issues/63#issuecomment-3471636364
// 代码作者：jiubanqingchen

import type { Plugin } from 'vite';

/**
 * 移除 element-plus-x 污染的 element-plus 样式
 * @see https://github.com/element-plus-x/Element-Plus-X/issues/63
 */
export function excludeCSSPlugin(): Plugin {
  return {
    name: 'exclude-css',
    enforce: 'pre',
    async resolveId(id: string) {
      const elxPrefix = '/vue-element-plus-x';
      if (id.includes(elxPrefix) && id.includes('node_modules')) {
        // 完全排除 element-plus-x 原有样式，重新编写
        return { id: '\0exclude-css:' + id, external: true };
        //兼容 pnpm
        const arr = id.split('node_modules');
        const lastPath = arr[arr.length - 1];
        const endPath = lastPath.substring(lastPath.indexOf(elxPrefix), lastPath.length);
        const excludeCSS = [elxPrefix + '/dist/base.css'];
        if (endPath.startsWith(elxPrefix + '/dist/el-') || excludeCSS.includes(endPath)) {
          return { id: '\0exclude-css:' + id, external: true };
        }
      }
    },
    load(id: string) {
      if (id.startsWith('\0exclude-css:')) {
        return '';
      }
    }
  };
}
