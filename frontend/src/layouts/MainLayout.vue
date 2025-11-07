<template>
  <q-layout view="lHh Lpr lFf" class="green-skin">
    <BackgroundSVG />

    <q-header elevated class="navbar-transparent" :class="{ 'is-scrolled': scrolled }">
      <q-toolbar>
        <q-toolbar-title class="cursor-pointer brand-title" @click="$router.push('/')">
          Te Liga!
        </q-toolbar-title>

        <div v-if="!$q.screen.lt.md" class="row items-center q-gutter-sm">
          <q-btn flat dense :to="{ name: 'mapa' }" label="Mapa" icon="map" class="nav-link" />

          <template v-if="isAuthenticated">
            <q-btn flat dense to="/mochila" label="Mochila" icon="inventory" class="nav-link" />
            <q-btn v-if="isAdmin" flat dense label="Admin" icon="admin_panel_settings" to="/admin/eventos" class="nav-link" />
            <q-btn flat dense :label="`Olá, ${userName}`" icon="account_circle" class="nav-link">
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

          <template v-else>
            <q-btn flat dense to="/login" label="Login" icon="login" class="nav-link" />
            <q-btn flat dense to="/register" label="Cadastro" icon="person_add" class="nav-link" />
          </template>

          <q-btn flat dense to="/teste-back" label="Testar API" icon="link" class="nav-link" />
        </div>

        <div v-else>
          <q-btn flat round dense icon="menu" class="nav-link" @click="drawerOpen = !drawerOpen" />
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="drawerOpen" side="right" overlay bordered class="bg-white text-dark">
      <q-list>
        <q-item clickable v-ripple to="mapa" @click="drawerOpen = false">
          <q-item-section avatar><q-icon name="map" /></q-item-section>
          <q-item-section>Mapa</q-item-section>
        </q-item>

        <template v-if="isAuthenticated">
          <q-item clickable v-ripple to="/mochila" @click="drawerOpen = false">
            <q-item-section avatar><q-icon name="inventory" /></q-item-section>
            <q-item-section>Mochila</q-item-section>
          </q-item>

          <q-item v-if="isAdmin" clickable v-ripple to="/admin/eventos" @click="drawerOpen = false">
            <q-item-section avatar><q-icon name="admin_panel_settings" /></q-item-section>
            <q-item-section>Admin</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/profile" @click="drawerOpen = false">
            <q-item-section avatar><q-icon name="account_circle" /></q-item-section>
            <q-item-section>Perfil</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="handleLogout">
            <q-item-section avatar><q-icon name="logout" /></q-item-section>
            <q-item-section>Sair</q-item-section>
          </q-item>
        </template>

        <template v-else>
          <q-item clickable v-ripple to="/login" @click="drawerOpen = false">
            <q-item-section avatar><q-icon name="login" /></q-item-section>
            <q-item-section>Login</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/register" @click="drawerOpen = false">
            <q-item-section avatar><q-icon name="person_add" /></q-item-section>
            <q-item-section>Cadastro</q-item-section>
          </q-item>
        </template>

        <q-separator spaced />
        <q-item clickable v-ripple to="/teste-back" @click="drawerOpen = false">
          <q-item-section avatar><q-icon name="link" /></q-item-section>
          <q-item-section>Testar API</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container class="page-container">
      <router-view />
    </q-page-container>

    <q-footer class="footer-transparent text-dark">
      <div class="text-center">© 2025 Te Liga!</div>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import BackgroundSVG from 'components/BackgroundGlobal.vue'

defineOptions({ name: 'MainLayout' })

const router = useRouter()
const route = useRoute()
const $q = useQuasar()

const isAuthenticated = ref(false)
const user = ref(null)
const drawerOpen = ref(false)
const scrolled = ref(false)

const isAdmin = computed(() => user.value?.is_staff === true)
const userName = computed(() => user.value?.first_name || user.value?.username || 'Usuário')

function updateUserState () {
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
  drawerOpen.value = false
}

function handleScroll () {
  scrolled.value = window.scrollY > 8
}

onMounted(() => {
  updateUserState()
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

watch(() => route.path, updateUserState)
</script>

<style scoped>
.green-skin{
  --ink:#0a1b0d;
  color: var(--ink);
  position: relative;
  z-index: 1;
}

.navbar-transparent{
  background: transparent !important;
  color: var(--ink);
  transition: background-color .2s ease, box-shadow .2s ease, color .2s ease;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}
.navbar-transparent.is-scrolled{
  background: rgba(255,255,255,.6) !important;
  box-shadow: 0 6px 18px rgba(0,0,0,.06);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.page-container{
  position: relative;
  z-index: 1;
  padding-top: 0;
}

.footer-transparent{
  background: transparent !important;
  color: var(--ink);
  border-top: 1px solid rgba(0,0,0,0.06);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  padding: 10px 12px;
}

:deep(.q-header .q-btn.nav-link){
  color: var(--ink) !important;
  font-weight: 700;
}
:deep(.q-header .q-btn.nav-link .q-icon){ opacity: .9; }

.brand-title{ color: var(--ink); font-weight: 800; letter-spacing: .2px; }

:deep(.q-header .q-btn.nav-link:focus-visible){
  outline: 2px solid rgba(59,130,246,.6);
  outline-offset: 2px;
}

.cursor-pointer{ cursor: pointer; }
</style>
