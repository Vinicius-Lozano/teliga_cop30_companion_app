<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="navbar-custom">
      <q-toolbar>
        <q-toolbar-title>Te Liga!</q-toolbar-title>
        <div>
          <q-btn flat dense to="/" label="Mapa" icon="map" />

          <!-- SEÇÃO PARA USUÁRIOS LOGADOS -->
          <template v-if="isAuthenticated">
            <q-btn flat dense to="/mochila" label="Mochila" icon="inventory" />
            
            <!-- Botão Admin (só aparece se o usuário for staff) -->
            <q-btn
              v-if="isAdmin"
              flat
              dense
              label="Admin"
              icon="admin_panel_settings"
              to="/admin/eventos"
            />

            <!-- Menu do Usuário -->
            <q-btn flat dense :label="`Olá, ${userName}`" icon="account_circle">
              <q-menu>
                <q-list style="min-width: 100px">
                  <q-item v-close-popup clickable @click="handleLogout">
                    <q-item-section>Sair</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </template>

          <!-- SEÇÃO PARA VISITANTES -->
          <template v-else>
            <q-btn flat dense to="/login" label="Login" icon="login" />
            <q-btn flat dense to="/register" label="Cadastro" icon="person_add" />
          </template>

          <q-btn flat dense to="/teste-back" label="Testar API" icon="link" />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="navbar-custom text-white q-py-sm">
      <div class="text-center">© 2025 Te Liga!</div>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

defineOptions({
  name: 'MainLayout'
})

const router = useRouter()
const route = useRoute()

// 1. Criar estado reativo local para substituir a store
const isAuthenticated = ref(false)
const user = ref(null)

// 2. Criar computeds que dependem do estado local
const isAdmin = computed(() => user.value?.is_staff === true)
const userName = computed(() => {
  if (!user.value) return 'Usuário'
  // Opcional: use o primeiro nome se disponível, senão o username
  return user.value.first_name || user.value.username
})

// 3. Função para ler o localStorage e atualizar o estado reativo
const updateUserState = () => {
  const token = localStorage.getItem('user_token')
  const userDataString = localStorage.getItem('user_data')
  isAuthenticated.value = !!token
  user.value = userDataString ? JSON.parse(userDataString) : null
}

// 4. Atualizar a função de logout
function handleLogout () {
  localStorage.removeItem('user_token')
  localStorage.removeItem('user_data')
  updateUserState() // Atualiza a UI imediatamente
  router.push('/login')
}

// 5. Garantir que o estado seja verificado quando o layout é montado...
onMounted(() => {
  updateUserState()
})

// 6. ...e também quando a rota muda (para refletir login/logout sem precisar recarregar a página)
watch(
  () => route.path,
  () => {
    updateUserState()
  }
)
</script>

<style scoped>
.navbar-custom {
  background: #2e7d32; /* Verde do banner da Home */
}
</style>
