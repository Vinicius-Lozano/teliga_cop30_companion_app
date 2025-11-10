import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { Notify } from 'quasar' // Importar o Quasar Notify

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})


// --- INTERCEPTOR DE REQUISIÇÃO ---
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

// --- INTERCEPTOR DE RESPOSTA ---
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

/**
 * syncLocalMochilaToBackend
 * - Lê possíveis chaves no localStorage onde dados antigos podem estar (ex: 'mochila', 'mochila_eventos', 'mochila_itens', 'mochila_pocoes')
 * - Tenta dar POST para as rotas do backend correspondentes.
 * - Remove as chaves locais quando sincronização conclui (ou parcialmente conclui).
 *
 * Observações:
 * - Deve ser chamado **após** o login bem-sucedido (ou quando houver token armazenado),
 *   para que o interceptor já inclua o Authorization header.
 * - A função ignora erros por item (continua com os próximos) para não travar toda a migração.
 */
export async function syncLocalMochilaToBackend() {
  try {
    const token = localStorage.getItem('user_token')
    if (!token) {
      // sem token — não faz sync
      return
    }

    // Checa várias chaves possíveis (compatibilidade com versões antigas)
    const possibleKeys = ['mochila', 'mochila_eventos', 'mochila_itens', 'mochila_pocoes']
    let combined = []

    for (const key of possibleKeys) {
      try {
        const raw = localStorage.getItem(key)
        if (!raw || raw === "undefined") continue
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) combined = combined.concat(parsed)
      } catch (e) {
        // se parsing falhar, apenas logamos e seguimos
        console.warn(`Não foi possível parsear ${key}:`, e)
      }
    }

    // Se não houver nada para migrar, sai
    if (combined.length === 0) return

    // Percorre os itens combinados e tenta migrar
    for (const entry of combined) {
      try {
        // Determine tipo do entry de forma robusta:
        // - se possuir campo tipoConteudo -> usa isso
        // - se possuir campo tipo === 'POC' -> trata como poção
        // - se possuir campos evento_id/item_id já -> pula (possivelmente já formatado)
        if (entry.evento_id || entry.tipoConteudo === 'evento' || entry.tipo === 'EVENT') {
          const eventoId = entry.evento_id ?? entry.id
          if (eventoId) {
            await api.post('/api/capturas/eventos/', { evento_id: eventoId })
          }
          continue
        }

        if (entry.item_id || entry.tipoConteudo === 'item' || (entry.tipo && entry.tipo !== 'POC')) {
          const itemId = entry.item_id ?? entry.id
          if (itemId) {
            await api.post('/api/capturas/items/', { item_id: itemId })
          }
          continue
        }

        // Tratamento específico para poções (POC)
        if (entry.pocao_id || entry.tipo === 'POC' || entry.tipoConteudo === 'pocao') {
          const pocaoId = entry.pocao_id ?? entry.id
          if (pocaoId) {
            await api.post('/api/capturas/pocoes/', { pocao_id: pocaoId })
          } else {
            // fallback: se entry possui id mas fora do padrão
            if (entry.id) await api.post('/api/capturas/pocoes/', { pocao_id: entry.id })
          }
          continue
        }

        // Se não conseguimos inferir, tentamos um POST genérico em items (fallback)
        if (entry.id) {
          await api.post('/api/capturas/items/', { item_id: entry.id })
        }
      } catch (e) {
        // Log e segue (não interrompe toda a sincronização)
        console.warn('Falha ao migrar entry para backend (seguindo adiante):', e, entry)
      }
    }

    // Se chegou até aqui, remove as chaves locais antigas (limpeza)
    for (const key of possibleKeys) {
      localStorage.removeItem(key)
    }

    // Também remove a chave 'mochila' se houver (compatibilidade extra)
    localStorage.removeItem('mochila')

    // Notifica o usuário de uma sincronização bem-sucedida (silenciosa se preferir)
    Notify.create({
      message: 'Mochila sincronizada com o servidor.',
      color: 'positive',
      position: 'top'
    })
  } catch (err) {
    console.error('Erro ao sincronizar localStorage com backend:', err)
    // Notifica mas não é crítico
    Notify.create({
      message: 'Problema ao sincronizar a mochila. Alguns itens podem não ter sido migrados.',
      color: 'warning',
      position: 'top'
    })
  }
}

export default boot(({ app }) => {
  app.config.globalProperties.$api = api
})

export { api }
