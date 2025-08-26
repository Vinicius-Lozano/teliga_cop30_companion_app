<template>
  <q-page class="flex flex-center bg-grey-2">
    <div class="register-container">

      <!-- Título -->
      <div class="title-container">
        <h1 class="title-te-liga">Te liga!</h1>
      </div>

      <q-card class="register-card">
        <q-card-section>
          <h2 class="text-center text-dark text-h6 q-mb-sm">
            Criar uma nova conta
          </h2>

          <q-input outlined label="Nome de usuário" dense class="q-mb-md" v-model="username" />

          <!-- data de nasscimento -->
          <div class="q-mb-sm text-dark">Data de nascimento</div>
          <div class="row q-col-gutter-sm q-mb-md">
            <q-input outlined label="Dia" dense class="col" v-model="day" />
            <q-input outlined label="Mês" dense class="col" v-model="month" />
            <q-input outlined label="Ano" dense class="col" v-model="year" />
          </div>

          <!-- genero -->
          <div class="q-mb-sm text-dark">Gênero</div>
          <div class="row justify-around q-mb-md">
            <q-radio dense v-model="gender" val="masculino" label="Masculino" />
            <q-radio dense v-model="gender" val="feminino" label="Feminino" />
            <q-radio dense v-model="gender" val="outro" label="Outro" />
          </div>

          <div>
            <q-input outlined label="Email" dense class="q-mb-md" v-model="email" />
            <q-input outlined label="Telefone" dense class="q-mb-md" v-model="telefone" />
          </div>

          <q-input outlined type="password" label="Crie uma Senha" dense class="q-mb-md" v-model="password" />
          <q-input outlined type="password" label="Confirme sua Senha" dense class="q-mb-md" v-model="confirmPassword" />

          <!-- botão de cadastro -->
          <div class="flex flex-center q-mt-md">
            <q-btn
              rounded
              label="Cadastre-se"
              class="register-btn"
              unelevated
              @click="handleRegister"
            />
          </div>

          <!-- link para login -->
          <div class="text-center q-mt-md">
            <a href="#/login" class="login-link">Já possui uma conta?</a>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import 'src/css/register.scss'
import { api } from 'boot/axios'

export default {
  name: "RegisterPage",
  data() {
    return {
      gender: 'masculino',
      username: '',
      day: '',
      month: '',
      year: '',
      email: '',
      telefone: '',
      password: '',
      confirmPassword: '',
    }
  },
  methods: {
    async handleRegister() {
      // --- Validação básica ---
      if (!this.email || !this.username || !this.password) {
        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: 'Por favor, preencha todos os campos obrigatórios.'
        })
        return
      }
      if (this.password !== this.confirmPassword) {
        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: 'As senhas não coincidem.'
        })
        return
      }

      const genderMap = { masculino: 'M', feminino: 'F', outro: 'O' }

      // --- Preparar os dados para a API ---
      const payload = {
        username: this.username,
        email: this.email,
        telefone: this.telefone || null,
        password1: this.password,
        password2: this.confirmPassword, 
        genero: genderMap[this.gender],
        data_nas: this.year && this.month && this.day
          ? `${this.year}-${String(this.month).padStart(2, '0')}-${String(this.day).padStart(2, '0')}`
          : null,
      }

      // --- Enviar para a API ---
      try {
        await api.post('/api/auth/registration/', payload)

        this.$q.notify({
          color: 'positive',
          position: 'top',
          message: 'Cadastro realizado com sucesso! Redirecionando para o login...'
        })

        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } catch (error) {
        let errorMessage = 'Ocorreu um erro no cadastro. Tente novamente.'
        const errorData = error.response?.data

        if (errorData) {
          if (typeof errorData === 'string') {
            errorMessage = errorData
          } else if (typeof errorData === 'object') {
            // Lida com erros de validação do DRF: { campo: ['mensagem'] }
            const errorList = Object.entries(errorData).map(([key, value]) => {
              const messages = Array.isArray(value) ? value.join(', ') : value;
              return `${key}: ${messages}`;
            });
            if (errorList.length) {
              errorMessage = errorList.join('\n');
            }
          }
        } else if (error.message) {
            errorMessage = error.message;
        }

        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: errorMessage.replace(/\n/g, '<br>'),
          html: true
        })
      }
    }
  }
}
</script>
