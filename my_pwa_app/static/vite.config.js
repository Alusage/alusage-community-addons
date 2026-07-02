import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: './src/main.jsx'
      },
      output: {
        entryFileNames: 'index.js',
        chunkFileNames: '[name].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'index.css'
          }
          return '[name].[ext]'
        }
      }
    },
    // Configuration pour Odoo
    manifest: false,
    sourcemap: false
  },
  base: '/my_pwa_app/static/dist/',
  server: {
    port: 3000,
    host: '0.0.0.0'
  }
})