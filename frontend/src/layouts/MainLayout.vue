<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="navbar-custom">
      <q-toolbar>
        <q-toolbar-title>Te Liga!</q-toolbar-title>
        <div>
          <q-btn flat dense to="/" label="Mapa" icon="map" />

          <template v-if="authStore.isAuthenticated">
            <q-btn
              v-if="authStore.isAdmin"
              flat
              dense
              label="Admin"
              icon="admin_panel_settings"
              to="/admin/eventos"
            />

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
import { computed } from 'vue'
import { useRouter } from 'vue-router'
// 1. Corrigir a importação da store
import { useAuthStore } from 'src/stores/auth'

defineOptions({
  name: 'MainLayout'
})

const router = useRouter()
// 2. Instanciar a store (ESSENCIAL!)
const authStore = useAuthStore()

const userName = computed(() => {
  if (!authStore.user) return 'Usuário'
  return authStore.user.first_name || authStore.user.username
})

function handleLogout () {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar-custom {
  background: #2e7d32; /* Verde do banner da Home */
}
</style>