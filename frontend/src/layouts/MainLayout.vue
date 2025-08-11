<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="navbar-custom">
      <q-toolbar>
        <q-toolbar-title>Te Liga!</q-toolbar-title>
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
defineOptions({
  name: 'MainLayout'
})
// Nenhum import ou variável necessária por enquanto
</script>

<style scoped>
.navbar-custom {
  background: #2e7d32; /* Este é o verde que usamos no banner da Home */
}
</style>
