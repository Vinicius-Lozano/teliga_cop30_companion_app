import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { Notify } from 'quasar' // Importar o Quasar Notify

const api = axios.create()

// --- INTERCEPTOR DE REQUISIÇÃO (Já estava correto) ---
// Adiciona o token em cada requisição
api.interceptors.request.use(config => {
  const token = localStorage.getItem('user_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// --- NOVO: INTERCEPTOR DE RESPOSTA ---
// Lida com erros globais, como tokens expirados
api.interceptors.response.use(
  // Se a resposta for bem-sucedida, apenas a retorne
  (response) => response,
  // Se ocorrer um erro...
  (error) => {
    // Verifica se o erro é de 'token inválido'
    if (error.response && error.response.status === 401 && error.response.data?.code === 'token_not_valid') {
      
      // 1. Limpa os dados inválidos do localStorage
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_data')

      // 2. Mostra uma notificação amigável para o usuário
      Notify.create({
        message: 'Sua sessão expirou. Por favor, faça o login novamente.',
        color: 'warning',
        icon: 'warning',
        position: 'top'
      })
      
      // 3. Redireciona para a página de login
      // Usamos 'window.location.href' para forçar um recarregamento completo da página
      // e garantir que o estado da aplicação seja limpo.
      window.location.href = '/#/login'
    }

    // Para todos os outros erros, apenas os rejeite para que o componente local possa tratá-los
    return Promise.reject(error)
  }
)


export default boot(({ app }) => {
  app.config.globalProperties.$api = api
})

export { api }

