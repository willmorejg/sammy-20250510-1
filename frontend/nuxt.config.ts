// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },

  modules: [
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@nuxtjs/google-fonts',
    'nuxt-bootstrap-icons',
  ],
  googleFonts: {
    families: {
      'Roboto Condensed': [300, 400, 500, 700],
      Roboto: [300, 400, 500, 700],
      Inter: [300, 400, 500, 700],
    },
    display: 'swap',
    preload: true,
    prefetch: true,
    preconnect: true,
    download: false
  },
  typescript: {
    strict: true
  },
  imports: {
    dirs: ['models'] // auto-import from '/...' directories
  },
  runtimeConfig: {
    public: {
      siteTitle: 'SAMmy',
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    }
  },
  plugins: ['~/plugins/bootstrap.client.ts', '~/plugins/popper.client.ts'],
  ssr: true,
  app: {
    baseURL: '/ui/',
    head: {
      title: 'SAMmy',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Management system for components and systems' }
      ]
    }
  },
  bootstrapIcons: {
    display: "inline", // or 'component'
    prefix: "bi", // prefix for the icon name
  },
  css: [
    'bootstrap/dist/css/bootstrap.min.css',
    'bootstrap-icons/font/bootstrap-icons.css',
    '~/assets/css/main.css'
  ],
})