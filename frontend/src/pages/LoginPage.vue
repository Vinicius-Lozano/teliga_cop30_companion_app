<template>
  <q-page class="flex bg-grey-2">

    <div class="column justify-center items-start q-pa-xl" style="flex: 1;">
      <div class="text-h2 text-green-10 font-weight-bold">Te liga!</div>
      <div class="text-subtitle1 text-black q-mt-xs">COP 30</div>
    </div>

    <div class="column justify-center items-center" style="flex: 1;">
      <q-card class="q-pa-lg" style="width: 84%; max-width: 432px;">
        
        <q-card-section class="text-center q-pb-sm">
          <div class="text-h4 text-green-10 font-weight-bold">Bem Vindo!</div>
          <div class="text-subtitle2 q-mt-xs">Efetue seu login</div>
        </q-card-section>

        <!-- Seção de Login Social (mantida como está) -->
        <q-card-section class="q-py-sm">
          <div class="row justify-center q-gutter-sm">
            <q-btn round flat size="lg" class="bg-white shadow-2" type="a" :href="URL_LOGIN_FACEBOOK">
              <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/facebook/facebook-original.svg"
                   alt="Facebook" width="22" height="22" />
            </q-btn>
            <q-btn round flat size="lg" class="bg-white shadow-2" type="a" :href="URL_LOGIN_GOOGLE">
              <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg"
                   alt="Google" width="22" height="22" />
            </q-btn>
          </div>
        </q-card-section>

        <!-- Formulário de Login -->
        <q-card-section class="q-pt-sm" tag="form" @submit.prevent="handleLogin">
          <q-input v-model="username" label="Usuário ou Email" outlined dense class="q-mb-sm" />
          <q-input v-model="password" label="Senha" type="password" outlined dense class="q-mb-sm" />

          <q-btn label="Acessar" color="green-10" rounded class="full-width q-mb-sm" type="submit" :loading="isLoading" />

          <div class="text-subtitle2 text-center q-mb-sm">
            Esqueceu a senha?
            <span class="text-primary" style="cursor: pointer;">Clique Aqui</span>
          </div>

          <div class="row justify-center">
            <q-btn label="Criar conta" color="purple" rounded to="/register" style="width: 60%; font-size: 0.9rem;" />
          </div>
        </q-card-section>
      </q-card>
    </div>

  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
// 1. Importar a instância 'api' configurada do axios
import { api } from 'boot/axios'

const $q = useQuasar()
const router = useRouter()

const username = ref('')
const password = ref('')
const isLoading = ref(false)

// URLs de Login Social (mantidas como estão)
const URL_LOGIN_GOOGLE = `${import.meta.env.VITE_API_URL}/auth/google`
const URL_LOGIN_FACEBOOK = `${import.meta.env.VITE_API_URL}/auth/facebook`

async function handleLogin () {
  if (!username.value || !password.value) {
    $q.notify({
      color: 'warning',
      message: 'Por favor, preencha o usuário e a senha.',
      icon: 'warning'
    })
    return
  }

  isLoading.value = true

  try {
    // 2. FAZER A CHAMADA DIRETA PARA A API
    const response = await api.post('/api/auth/login/', {
      username: username.value,
      password: password.value
    })

    // 3. SALVAR OS DADOS NO LOCALSTORAGE
    // A resposta da dj-rest-auth com JWT inclui 'access' (o token) e 'user' (os dados do usuário)
    localStorage.setItem('user_token', response.data.access)
    localStorage.setItem('user_data', JSON.stringify(response.data.user))
    
    // 4. REDIRECIONAR EM CASO DE SUCESSO
    router.push('/')

  } catch (error) {
    // 5. MOSTRAR O ERRO EM CASO DE FALHA
    console.error('Falha no login:', error)
    $q.notify({
      color: 'negative',
      message: 'Usuário ou senha inválidos. Tente novamente.',
      icon: 'report_problem'
    })
  } finally {
    isLoading.value = false
  }
}
</script>