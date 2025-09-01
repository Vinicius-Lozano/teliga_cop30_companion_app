import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { useAuthStore } from 'src/stores/auth' // 1. Importar o auth store

// A URL base da sua API Django
// Removido, pois o proxy do devServer cuida disso.
// Para produção, você configurará isso de outra forma (ex: variáveis de ambiente).
const baseURL = ''

// Criamos uma instância do axios que será usada em toda a aplicação
const api = axios.create({ baseURL })

// 2. Criar um interceptor de requisições
api.interceptors.request.use(config => {
  // --- DEBUGGING ---
  console.log('[Axios Interceptor] Interceptando requisição para:', config.url)

  // É preciso instanciar a store DENTRO do interceptor
  const authStore = useAuthStore()
  const token = authStore.token

  // --- DEBUGGING ---
  console.log('[Axios Interceptor] Token encontrado no authStore:', token)

  // Se o token existir, adiciona o cabeçalho de autorização
  if (token) {
    // --- DEBUGGING ---
    console.log('[Axios Interceptor] Token encontrado. Adicionando cabeçalho de autorização.')
    // O formato 'Bearer' é o padrão para JWT com dj-rest-auth
    config.headers.Authorization = `Bearer ${token}`
  } else {
    // --- DEBUGGING ---
    console.warn('[Axios Interceptor] Nenhum token encontrado. A requisição não será autorizada.')
  }

  return config
}, error => {
  // Faz algo com o erro da requisição
  return Promise.reject(error)
})

export default boot(({ app }) => {
  // Para uso dentro de arquivos Vue (Options API) através de this.$api
  app.config.globalProperties.$api = api
})

// Exportamos a instância `api` para que possamos importá-la
// diretamente em qualquer arquivo JS/Vue.
export { api }

