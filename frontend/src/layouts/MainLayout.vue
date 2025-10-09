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

            <!-- Menu do Usuário com Perfil -->
            <q-btn flat dense :label="`Olá, ${userName}`" icon="account_circle">
              <q-menu>
                <q-list style="min-width: 150px">
                  <q-item v-close-popup clickable @click="$router.push('/profile')">
                    <q-item-section>Perfil</q-item-section>
                  </q-item>
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

const isAuthenticated = ref(false)
const user = ref(null)

const isAdmin = computed(() => user.value?.is_staff === true)
const userName = computed(() => {
  if (!user.value) return 'Usuário'
  return user.value.first_name || user.value.username
})

const updateUserState = () => {
  const token = localStorage.getItem('user_token')
  const userDataString = localStorage.getItem('user_data')
  isAuthenticated.value = !!token
  user.value = userDataString ? JSON.parse(userDataString) : null
}

function handleLogout () {
  localStorage.removeItem('user_token')
  localStorage.removeItem('user_data')
  updateUserState()
  router.push('/login')
}

onMounted(() => {
  updateUserState()
})

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

