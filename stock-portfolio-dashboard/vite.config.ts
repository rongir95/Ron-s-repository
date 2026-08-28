import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Yahoo Finance's public endpoints send no CORS headers, so the browser cannot
 * call them directly. Instead of shipping a server, we proxy them same-origin:
 *
 *   dev / preview  -> the Vite proxy below
 *   Vercel         -> vercel.json  rewrite
 *   Netlify        -> netlify.toml  redirect (status 200 = proxy)
 *
 * All three map `/yf/*` onto `https://query1.finance.yahoo.com/*`, so the client
 * code is identical everywhere and needs no API key.
 */
const yahooProxy = {
  '/yf': {
    target: 'https://query1.finance.yahoo.com',
    changeOrigin: true,
    rewrite: (path: string) => path.replace(/^\/yf/, ''),
  },
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: { proxy: yahooProxy },
  preview: { proxy: yahooProxy },
})
