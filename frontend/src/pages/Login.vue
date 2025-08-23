<template>
  <q-page class="flex bg-grey-2">

    <div class="column justify-center items-start q-pa-xl" style="flex: 1;">
      <div class="text-h2 text-green-10 font-weight-bold">Te liga!</div>
      <div class="text-subtitle1 text-black q-mt-xs">COP 30</div>
    </div>

    <div class="column justify-center items-center" style="flex: 1;">
      <q-card class="q-pa-lg" style="width: 84%; max-width: 432px;">
        
        <!-- titulo do card -->
        <q-card-section class="text-center q-pb-sm">
          <div class="text-h4 text-green-10 font-weight-bold">Bem Vindo!</div>
          <div class="text-subtitle2 q-mt-xs">Efetue seu login</div>
        </q-card-section>

        <q-card-section class="q-py-sm">
          <div class="row justify-center q-gutter-sm">
        
            <q-btn round flat size="lg" class="bg-white shadow-2">
              <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/facebook/facebook-original.svg" 
                   alt="Facebook" width="22" height="22" />
            </q-btn>

            <q-btn round flat size="lg" class="bg-white shadow-2">
              <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" 
                   alt="Google" width="22" height="22" />
            </q-btn>
          </div>
        </q-card-section>

        <!-- Formulario -->
        <q-card-section class="q-pt-sm">
          <q-input v-model="email" label="Email ou usuário" outlined dense class="q-mb-sm" />
          <q-input v-model="password" label="Senha" type="password" outlined dense class="q-mb-sm" />
          
          <q-btn label="Acessar" color="green-10" rounded class="full-width q-mb-sm" />
          
          <div class="text-subtitle2 text-center q-mb-sm">
            Esqueceu a senha? 
            <span class="text-primary" style="cursor: pointer;">Clique Aqui</span>
          </div>

          <div class="row justify-center">
            <q-btn label="Criar conta" color="purple" rounded style="width: 60%; font-size: 0.9rem;" />
          </div>
        </q-card-section>

      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

// URL
const URL_LOGIN_GOOGLE = import.meta.env.VITE_API_URL + '/auth/google'
const URL_LOGIN_FACEBOOK = import.meta.env.VITE_API_URL + '/auth/facebook'

console.log(URL_LOGIN_GOOGLE, URL_LOGIN_FACEBOOK)
</script>

<style scoped>
.text-green-10 {
  color: #2e7d32;
}
.font-weight-bold {
  font-weight: 700;
}
.text-black {
  color: #000000;
}
</style>
