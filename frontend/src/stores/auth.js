import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'

// Definindo a URL base da API a partir das variáveis de ambiente
const API_URL = import.meta.env.VITE_API_URL

export const useAuthStore = defineStore('auth', () => {
  // --- STATE ---
  const token = ref(localStorage.getItem('accessToken') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)

  // Configura o header do axios sempre que o token mudar
  if (token.value) {
    axios.defaults.headers.common.Authorization = `Bearer ${token.value}`
  }

  // --- GETTERS ---
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin === true || user.value?.is_staff === true)

  // --- ACTIONS ---
  async function login (credentials) {
    try {
      // 1. Faz a requisição de login
      const response = await axios.post(`${API_URL}/auth/login/`, credentials)

      // 2. Salva o token no estado e no localStorage
      token.value = response.data.access
      localStorage.setItem('accessToken', token.value)
      axios.defaults.headers.common.Authorization = `Bearer ${token.value}`

      // 3. Busca e salva os dados do usuário
      await fetchUser()

    } catch (error) {
      // Se der erro, limpa tudo e propaga o erro para o componente
      logout()
      throw error
    }
  }

  async function fetchUser () {
    if (!token.value) return

    try {
      const response = await axios.get(`${API_URL}/auth/user/`)
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch (error) {
      console.error('Falha ao buscar dados do usuário:', error)
      logout() // Se o token for inválido, desloga
    }
  }

  function logout () {
    token.value = null
    user.value = null
    localStorage.removeItem('accessToken')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common.Authorization
  }

  // Expõe o estado, getters e ações
  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    fetchUser
  }
})