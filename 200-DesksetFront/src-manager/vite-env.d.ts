/// <reference types="vite/client" />

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}


// 类型声明 import.meta.env.VITE_DESKSET_GITHUB_TOKEN
interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface ImportMetaEnv {
  readonly VITE_DESKSET_GITHUB_TOKEN: string;
}
