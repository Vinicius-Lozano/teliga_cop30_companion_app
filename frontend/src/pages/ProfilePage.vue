<template>
  <q-page class="bg-grey-2 profile-page">
    <div class="profile-header q-pa-md">
      <h1 class="text-green-10 text-h4 q-mb-xs">Te liga!</h1>
      <div class="row items-center cursor-pointer" @click="$router.push('/')">
        <q-icon name="arrow_back" color="green-10" size="20px" />
        <span class="text-green-10 text-subtitle2 q-ml-xs">Voltar ao início</span>
      </div>
    </div>

    <div class="flex flex-center q-pa-xl">
      <div class="register-container">
        <h1 class="text-h5 text-green-10 text-center q-mb-lg">Perfil</h1>

        <div class="row items-center justify-center q-mb-lg">
          <q-avatar size="80px" class="q-mr-md">
            <img :src="user.avatar || 'https://cdn-icons-png.flaticon.com/512/847/847969.png'" />
          </q-avatar>
          <div>
            <div class="text-green-10 user-name">{{ user.username }}</div>
            <div class="text-grey-7">{{ user.email }}</div>
          </div>
        </div>

        <div class="q-gutter-md info-container">
          <div class="perfil-campo">
            <span class="campo-label">Nome</span>
            <span class="campo-valor">{{ user.username }}</span>
          </div>
          <div class="perfil-campo">
            <span class="campo-label">Email</span>
            <span class="campo-valor">{{ user.email }}</span>
          </div>
          <div class="perfil-campo">
            <span class="campo-label">Idade</span>
            <span class="campo-valor">{{ user.idade }}</span>
          </div>
          <div class="perfil-campo">
            <span class="campo-label">Telefone</span>
            <span class="campo-valor">{{ user.telefone }}</span>
          </div>
        </div>

        <div class="column items-center q-mt-xl q-gutter-md action-buttons">
          <q-btn label="Editar perfil" color="green-10" class="full-width" rounded @click="editarPerfil" />
          <q-btn label="Alterar senha" color="green-10" class="full-width" rounded @click="abrirAlterarSenha" />
          <q-btn label="Excluir conta" color="purple-10" class="full-width" rounded @click="confirmarExclusao" />
        </div>
      </div>
    </div>

    <!-- Modal de alteração de senha -->
    <q-dialog v-model="senhaDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Alterar senha</div>
          <q-input v-model="oldPassword" label="Senha atual" type="password" dense />
          <q-input v-model="newPassword" label="Nova senha" type="password" dense />
          <q-input v-model="confirmPassword" label="Confirme a nova senha" type="password" dense />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="grey" v-close-popup @click="senhaDialog=false" />
          <q-btn flat label="Alterar" color="green-10" @click="alterarSenha" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Modal confirmação exclusão -->
    <q-dialog v-model="excluirDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Excluir conta</div>
          <div>Tem certeza que deseja excluir sua conta? Esta ação não poderá ser desfeita.</div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="grey" v-close-popup />
          <q-btn flat label="Excluir" color="purple-10" @click="excluirConta" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'
import { LocalStorage, useQuasar } from 'quasar'
import 'src/css/profile.scss' 

const $q = useQuasar()
const router = useRouter()

const user = ref({ username:'', email:'', idade:'', telefone:'', avatar:null })
const excluirDialog = ref(false)
const senhaDialog = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

onMounted(async () => {
  try {
    const token = LocalStorage.getItem('user_token')
    if (!token) { router.push('/login'); return }

    const { data } = await api.get('/api/auth/user/')
    user.value.username = data.username
    user.value.email = data.email
    user.value.idade = calcularIdade(data.data_nas)
    user.value.telefone = data.telefone || ''
    user.value.avatar = data.avatar || null
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao carregar perfil' })
    router.push('/login')
  }
})

function calcularIdade(data_nas) {
  if (!data_nas) return ''
  const nascimento = new Date(data_nas)
  const hoje = new Date()
  let idade = hoje.getFullYear() - nascimento.getFullYear()
  const m = hoje.getMonth() - nascimento.getMonth()
  if (m < 0 || (m === 0 && hoje.getDate() < nascimento.getDate())) idade--
  return idade
}

function editarPerfil() {
  $q.notify({ type: 'info', message: 'Função de edição de perfil ainda não implementada' })
}

function abrirAlterarSenha() {
  senhaDialog.value = true
}

async function alterarSenha() {
  if (newPassword.value !== confirmPassword.value) {
    $q.notify({ type:'negative', message:'As novas senhas não coincidem' })
    return
  }

  try {
    await api.put('/api/users/me/change_password/', {
      old_password: oldPassword.value,
      new_password: newPassword.value
    })
    $q.notify({ type:'positive', message:'Senha alterada com sucesso' })
    senhaDialog.value = false
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (e) {
    const msg = e.response?.data?.old_password || 'Erro ao alterar senha'
    $q.notify({ type:'negative', message: msg })
  }
}

function confirmarExclusao() { excluirDialog.value = true }

async function excluirConta() {
  try {
    await api.delete('/api/users/me/delete/')
    LocalStorage.remove('user_token')
    LocalStorage.remove('user_data')
    router.push('/login')
    $q.notify({ type:'positive', message:'Conta excluída com sucesso' })
  } catch (e) {
    console.error(e)
    $q.notify({ type:'negative', message:'Erro ao excluir conta' })
  }
  excluirDialog.value = false
}
</script>
















































