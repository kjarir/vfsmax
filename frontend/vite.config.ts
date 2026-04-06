import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/_/backend/api/v1': {
        target: 'http://127.0.0.1:8010',
        rewrite: (path) => path.replace(/^\/_\/backend/, ''),
        changeOrigin: true,
      }
    }
  }
})
