<template>
  <q-page class="container q-pa-md" v-if="item">
    <div class="row justify-end q-mb-md">
      <q-btn
        label="Detalhes"
        flat
        icon="arrow_back"
        :to="{ name: 'ItemDetalhes', params: { id: item.id } }"
      />
    </div>

    <q-card>
      <q-card-section horizontal>
        <q-card-section class="col-10">
          <h1
            class="q-mt-none q-mb-sm"
            style="color:#166534; font-size:36px; font-weight:900; line-height:1.1"
          >
            Capturar
          </h1>

          <div class="relative-position">
            <q-img :src="item.imagem" style="width:100%; height:600px" />

            <!-- animação BONK -->
            <transition name="fade">
              <img
                v-if="mostrarBonk"
                src="/effects/bonk.gif"
                alt="bonk"
                class="bonk-animacao"
              />
            </transition>

            <!-- animação OVO -->
            <transition name="fade">
              <img
                v-if="mostrarOvo"
                src="/effects/ovo.gif"
                alt="ovo"
                class="ovo-animacao"
              />
            </transition>
          </div>

          <q-card-section align="center">
            <q-linear-progress
              size="25px"
              :value="chance / 100"
              color="green"
              class="q-mt-md"
            >
              <div class="absolute-full flex flex-center text-white">
                {{ chance }}%
              </div>
            </q-linear-progress>

            <q-btn
              v-if="chance >= 100"
              label="Capturar"
              color="primary"
              class="q-mt-md"
              @click="capturar"
            />
          </q-card-section>
        </q-card-section>

        <q-separator vertical color="gray-4" />

        <q-card-actions vertical class="justify-center q-pa-lg">
          <q-btn label="Conversar" color="green" @click="abrirConversa" />
          <q-btn label="Paulada" color="red" @click="atacar" />
          <q-btn label="Ovo" color="red" @click="usarOvo" />
        </q-card-actions>
      </q-card-section>
    </q-card>

    <!-- Diálogo de conversa -->
    <q-dialog v-model="mostrarDialogo" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ questao?.pergunta }}</div>
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-list bordered>
            <q-item clickable v-for="(opcao, letra) in opcoes" :key="letra" @click="responder(letra)">
              <q-item-section>{{ letra }}) {{ opcao }}</q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <q-card v-if="resultado" class="q-mt-md">
        <q-card-section>
          <div
            :class="{
              'text-positive': resultado.acertou,
              'text-negative': !resultado.acertou
            }"
          >
            {{ resultado.acertou ? 'Você acertou!' : 'Errou! 😢' }}
          </div>
          <div v-if="resultado.resposta_correta">
            Resposta correta: {{ resultado.resposta_correta }}
          </div>
        </q-card-section>
        <q-card-actions align="center">
          <q-btn flat label="Fechar" color="primary" @click="fecharDialogo" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const route = useRoute()
const item = ref(null)
const isLoading = ref(true)
const chance = ref(0)

const mostrarDialogo = ref(false)
const questao = ref(null)
const resultado = ref(null)
const opcoes = ref({})
const mostrarBonk = ref(false)
const mostrarOvo = ref(false)

onMounted(async () => {
  const itemId = route.params.id
  if (itemId) {
    const [resItem, resCaptura] = await Promise.all([
      api.get(`/api/item/${itemId}/`),
      api.get(`/api/captura/${itemId}/`)
    ])
    item.value = resItem.data
    chance.value = resCaptura.data.chance
  }
  isLoading.value = false
})

async function executarAcao(acao) {
  try {
    const itemId = route.params.id
    const res = await api.post(`/api/captura/${itemId}/`, { acao })
    chance.value = res.data.chance
  } catch (err) {
    console.error(err)
    $q.notify({
      type: 'negative',
      message: 'Erro ao executar ação'
    })
  }
}

// === ATAQUE (com som e bonk)
async function atacar() {
  const som = new Audio('/sounds/bonk.mp3')
  som.volume = 0.8
  som.play().catch(err => console.warn('Erro ao tocar som:', err))

  mostrarBonk.value = true
  setTimeout(() => (mostrarBonk.value = false), 800) // esconde o bonk após 0.8s

  await executarAcao('atacar')
}

// === USAR OVO (sem som, mesma lógica de ataque)
async function usarOvo() {
  mostrarOvo.value = true
  setTimeout(() => (mostrarOvo.value = false), 1000) // esconde o ovo após 1s

  await executarAcao('atacar') // backend trata igual ao ataque
}

async function abrirConversa() {
  try {
    const itemId = route.params.id
    const res = await api.get(`/api/questao/item/${itemId}/`)
    questao.value = res.data
    opcoes.value = {
      A: res.data.escolha_a,
      B: res.data.escolha_b,
      C: res.data.escolha_c
    }
    mostrarDialogo.value = true
    resultado.value = null
  } catch (err) {
    console.error(err)
    $q.notify({ type: 'negative', message: 'Erro ao buscar questão' })
  }
}

async function responder(letra) {
  try {
    const res = await api.post(`/api/questao/${questao.value.id}/`, {
      resposta: letra
    })
    resultado.value = res.data

    if (res.data.acertou) {
      await executarAcao('conversar') // aumenta chance ao acertar
    }
  } catch (err) {
    console.error(err)
    $q.notify({ type: 'negative', message: 'Erro ao enviar resposta' })
  }
}

function fecharDialogo() {
  mostrarDialogo.value = false
  resultado.value = null
}

async function capturar() {
  try {
    const itemId = route.params.id
    const res = await api.post(`/api/captura/${itemId}/confirmar/`)
    $q.notify({
      type: 'positive',
      message: res.data.mensagem || 'Item capturado com sucesso!'
    })
    chance.value = 100
    const mochila = await api.get('/api/capturas/items/')
    console.log('Itens na mochila:', mochila.data)
  } catch (err) {
    console.error(err)
    $q.notify({
      type: 'negative',
      message: err.response?.data?.error || 'Erro ao capturar'
    })
  }
}
</script>

<style scoped>
.bonk-animacao,
.ovo-animacao {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  pointer-events: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
