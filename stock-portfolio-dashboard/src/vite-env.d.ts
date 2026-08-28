/// <reference types="vite/client" />

interface ImportMetaEnv {
  /**
   * Build-time default market-data provider ('yahoo' | 'twelvedata' | 'demo').
   * Only affects a fresh install with no saved settings; the user can always
   * change it in Settings. Used by the standalone build, which has no /yf proxy
   * and so cannot reach Yahoo Finance.
   */
  readonly VITE_DEFAULT_PROVIDER?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
