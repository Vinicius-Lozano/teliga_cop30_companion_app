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

        <q-card-section class="q-pt-sm" tag="form" @submit.prevent="handleLogin">
          <q-input v-model="username" label="Usuário" outlined dense class="q-mb-sm" />
          <q-input v-model="password" label="Senha" type="password" outlined dense class="q-mb-sm" />

          <q-btn label="Acessar" color="green-10" rounded class="full-width q-mb-sm" type="submit" />

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
// O axios não é mais necessário aqui, a store cuida disso
import { useAuthStore } from 'src/stores/auth'

// importação do css (se houver)
// import 'src/css/login.scss'

const $q = useQuasar()
const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

// URLs de Login Social (se aplicável)
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

  try {
    // 1. CHAME A AÇÃO DA STORE: A store agora é responsável por toda a lógica de API.
    await authStore.login({
      username: username.value,
      password: password.value
    })

    // 2. REDIRECIONE EM CASO DE SUCESSO
    router.push('/')

  } catch (error) {
    // 3. MOSTRE O ERRO EM CASO DE FALHA
    console.error('Falha no login:', error)
    $q.notify({
      color: 'negative',
      message: 'Usuário ou senha inválidos. Tente novamente.',
      icon: 'report_problem'
    })
  }
}
</script>