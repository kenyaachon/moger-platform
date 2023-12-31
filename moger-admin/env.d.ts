/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_REGION: string
  readonly VITE_USER_POOL_ID: string
  readonly VITE_USER_POOL_APP_CLIENT_ID: string
  readonly VITE_MOGER_PROXY_API: string
  // more env variables...
}
interface ImportMeta {
  readonly env: ImportMetaEnv
}
