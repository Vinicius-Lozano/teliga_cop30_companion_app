<template>
  <q-page class="flex bg-grey-2">

    <div class="column justify-center items-start q-pa-xl" style="flex: 1;">
      <div class="text-h2 text-green-10 font-weight-bold">Te liga!</div>
      <div class="text-subtitle1 text-black q-mt-xs">COP 30</div>
    </div>

    <div class="column justify-center items-center" style="flex: 1;">
      <q-card class="q-pa-lg" style="width: 84%; max-width: 432px;">
        
        <!-- título do card -->
        <q-card-section class="text-center q-pb-sm">
          <div class="text-h4 text-green-10 font-weight-bold">Bem Vindo!</div>
          <div class="text-subtitle2 q-mt-xs">Efetue seu login</div>
        </q-card-section>

        <!-- Botões de Login Social -->
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

        <!-- Formulário -->
        <q-card-section class="q-pt-sm" tag="form" @submit.prevent="login">
          <q-input v-model="username" label="Email ou usuário" outlined dense class="q-mb-sm" />
          <q-input v-model="password" label="Senha" type="password" outlined dense class="q-mb-sm" />

          <q-btn label="Acessar" color="green-10" rounded class="full-width q-mb-sm" type="submit" />

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
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { authStore } from 'src/stores/auth'

// importação do css
import 'src/css/login.scss'

const $q = useQuasar()
const router = useRouter()

const username = ref('')
const password = ref('')

// URLs de Login Social
const URL_LOGIN_GOOGLE = `${import.meta.env.VITE_API_URL}/auth/google`
const URL_LOGIN_FACEBOOK = `${import.meta.env.VITE_API_URL}/auth/facebook`

async function login () {
  if (!username.value || !password.value) {
    $q.notify({
      color: 'warning',
      textColor: 'black',
      message: 'Por favor, preencha o usuário e a senha.',
      icon: 'warning'
    })
    return
  }
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/login/`, {
      username: username.value,
      password: password.value
    })

    const accessToken = response.data.access
    const refreshToken = response.data.refresh
    // Armazena os tokens no localStorage
    localStorage.setItem('accessToken', accessToken)
    localStorage.setItem('refreshToken', refreshToken)

    // Define o header de autorização para as próximas requisições
    axios.defaults.headers.common.Authorization = `Bearer ${accessToken}`

    // Busca os dados do usuário
    const userResponse = await axios.get(`${import.meta.env.VITE_API_URL}/api/auth/user/`)
    authStore.setUser(userResponse.data)

    // Redireciona para a página principal
    router.push('/')
  } catch (error) {
    let errorMessage = 'Não foi possível fazer o login. Tente novamente.'
    if (error.response && error.response.status === 401) {
      errorMessage = 'Usuário ou senha inválidos.'
    }
    $q.notify({
      color: 'negative',
      message: errorMessage,
      icon: 'report_problem'
    })
  }
}
</script>