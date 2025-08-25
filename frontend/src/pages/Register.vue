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

          <!-- Nome e sobrenome -->
          <div class="row q-col-gutter-sm q-mb-md">
            <q-input outlined label="Nome" dense class="col" v-model="firstName" />
            <q-input outlined label="Sobrenome" dense class="col" v-model="lastName" />
          </div>

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

          <q-input outlined label="Celular ou Email" dense class="q-mb-md" v-model="emailOrCell" />

          <q-input outlined type="password" label="Crie uma Senha" dense class="q-mb-md" v-model="password" />

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
            <a href="/login" class="login-link">Já possui uma conta?</a>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import 'src/css/register.scss'

export default {
  name: "RegisterPage",
  data() {
    return {
      gender: null,
      firstName: '',
      lastName: '',
      day: '',
      month: '',
      year: '',
      emailOrCell: '',
      password: ''
    }
  },
  methods: {
    handleRegister() {
      console.log({
        firstName: this.firstName,
        lastName: this.lastName,
        day: this.day,
        month: this.month,
        year: this.year,
        gender: this.gender,
        emailOrCell: this.emailOrCell,
        password: this.password
      });
    }
  }
}
</script>

