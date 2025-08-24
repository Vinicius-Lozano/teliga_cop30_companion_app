import { reactive } from 'vue'
import axios from 'axios'

// Um objeto reativo simples para servir como nosso "store"
export const authStore = reactive({
  user: null,
  isAuthenticated: false,

  /**
   * Define os dados do usuário e atualiza o estado de autenticação.
   * @param {object | null} userData - Os dados do usuário ou null para logout.
   */
  setUser (userData) {
    this.user = userData
    this.isAuthenticated = !!userData
    if (userData) {
      // Armazena para persistir entre atualizações da página
      localStorage.setItem('user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('user')
    }
  },

  /**
   * Realiza o logout do usuário.
   */
  logout () {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    this.user = null
    this.isAuthenticated = false
    // Remove o header de autorização do axios
    delete axios.defaults.headers.common.Authorization
  },

  /**
   * Tenta inicializar o estado a partir do localStorage na primeira carga.
   */
  init () {
    const user = localStorage.getItem('user')
    if (user) {
      this.setUser(JSON.parse(user))
    }
  }
})

// Inicializa o store quando o módulo é carregado pela primeira vez
authStore.init()

