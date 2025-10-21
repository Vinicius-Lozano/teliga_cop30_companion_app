<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Fundo SVG -->
    <BackgroundSVG />

    <!-- Header -->
    <q-header elevated class="navbar-custom">
      <q-toolbar>

        <!-- Logo / título -->
        <q-toolbar-title
          class="cursor-pointer"
          @click="$router.push('/')"
        >
          Te Liga!
        </q-toolbar-title>

        <!-- DESKTOP NAV -->
        <div v-if="!$q.screen.lt.md" class="row items-center q-gutter-sm">
          <q-btn flat dense to="/" label="Mapa" icon="map" />

          <!-- Usuários logados -->
          <template v-if="isAuthenticated">
            <q-btn flat dense to="/mochila" label="Mochila" icon="inventory" />
            <q-btn
              v-if="isAdmin"
              flat dense
              label="Admin"
              icon="admin_panel_settings"
              to="/admin/eventos"
            />
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

          <!-- Visitantes -->
          <template v-else>
            <q-btn flat dense to="/login" label="Login" icon="login" />
            <q-btn flat dense to="/register" label="Cadastro" icon="person_add" />
          </template>

          <q-btn flat dense to="/teste-back" label="Testar API" icon="link" />
        </div>

        <!-- MOBILE NAV -->
        <div v-else>
          <q-btn
            flat
            round
            dense
            icon="menu"
            @click="drawerOpen = !drawerOpen"
          />
        </div>

      </q-toolbar>
    </q-header>

    <!-- DRAWER MOBILE -->
    <q-drawer
      v-model="drawerOpen"
      side="right"
      overlay
      bordered
      class="bg-white text-dark"
    >
      <q-list>
        <q-item clickable v-ripple to="/" @click="drawerOpen = false">
          <q-item-section avatar><q-icon name="map" /></q-item-section>
          <q-item-section>Mapa</q-item-section>
        </q-item>

        <template v-if="isAuthenticated">
          <q-item clickable v-ripple to="/mochila" @click="drawerOpen = false">
            <q-item-section avatar><q-icon name="inventory" /></q-item-section>
            <q-item-section>Mochila</q-item-section>
          </q-item>

          <q-item
            v-if="isAdmin"
            clickable v-ripple
            to="/admin/eventos"
            @click="drawerOpen = false"
          >
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

    <!-- Conteúdo das páginas -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <q-footer class="navbar-custom text-white q-py-sm">
      <div class="text-center">© 2025 Te Liga!</div>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
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

const isAdmin = computed(() => user.value?.is_staff === true)
const userName = computed(() => user.value?.first_name || user.value?.username || 'Usuário')

function updateUserState() {
  const token = localStorage.getItem('user_token')
  const userDataString = localStorage.getItem('user_data')
  isAuthenticated.value = !!token
  user.value = userDataString ? JSON.parse(userDataString) : null
}

function handleLogout() {
  localStorage.removeItem('user_token')
  localStorage.removeItem('user_data')
  updateUserState()
  router.push('/login')
  drawerOpen.value = false
}

onMounted(() => {
  updateUserState()
})

watch(() => route.path, updateUserState)
</script>

<style scoped>
.navbar-custom {
  background: #2e7d32;
  color: white;
}
.cursor-pointer {
  cursor: pointer;
}
</style>
