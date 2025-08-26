import { boot } from 'quasar/wrappers'
import axios from 'axios'

// A URL base da sua API Django
const baseURL = 'http://127.0.0.1:8000'

// Criamos uma instância do axios que será usada em toda a aplicação
const api = axios.create({ baseURL })

export default boot(({ app }) => {
  // Para uso dentro de arquivos Vue (Options API) através de this.$api
  app.config.globalProperties.$api = api

  // Para uso dentro de arquivos Vue (Composition API) através de inject
  // app.provide('api', api)
})

// Exportamos a instância `api` para que possamos importá-la
// diretamente em qualquer arquivo JS/Vue, como você fez no Register.vue
export { api }