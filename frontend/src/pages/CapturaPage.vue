<template>
  <q-page class="container q-pa-md position-relative green-bg">
    <q-card class="main-card">
      <q-card-section class="row no-wrap">
        <div class="col-7 card-image relative-position">
          <q-img :src="item?.imagem" class="main-img" />
          <transition name="fade">
            <img v-if="mostrarBonk" src="/effects/bonk.gif" class="bonk-animacao" />
          </transition>
          <transition name="fade">
            <img v-if="mostrarOvo" src="/effects/ovo.gif" class="ovo-animacao" />
          </transition>
        </div>

        <q-card-section class="col-5 actions-col column" style="height: 100%; align-items: flex-start;">
          <div class="row items-center q-mb-md">
            <q-icon name="backpack" color="green-8" size="28px" class="q-mr-sm" />
            <span class="text-h5" style="color:#166534; font-weight: 700;">Capturar</span>
          </div>

          <div style="flex-grow:1;"></div>

          <div class="column full-width">
            <q-btn
              v-for="habilidade in habilidades"
              :key="habilidade.id"
              :label="habilidade.nome"
              color="primary"
              :disable="habilidade.quantidade === 0"
              class="full-width q-mb-sm"
              @click="usarHabilidade(habilidade)"
            >
              <template v-slot:append>
                <span v-if="habilidade.quantidade !== null" class="text-subtitle2 q-ml-sm">
                  x{{ habilidade.quantidade }}
                </span>
              </template>
            </q-btn>

            <q-btn label="Conversar" color="green" icon="chat" @click="abrirConversa" class="full-width q-mb-sm" />
          </div>
        </q-card-section>
      </q-card-section>

      <q-card-section class="q-mt-md">
        <q-linear-progress
          :value="chance / 100"
          color="green-5"
          track-color="green-2"
          size="30px"
          class="progress-bar"
        >
          <div class="progress-text">{{ chance }}%</div>
        </q-linear-progress>

        <q-btn
          v-if="chance >= 100"
          label="Capturar"
          color="primary"
          class="q-mt-md full-width"
          @click="capturar"
        />
      </q-card-section>
    </q-card>

    <q-dialog v-model="mostrarDialogo" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ questao?.pergunta }}</div>
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-list bordered>
            <q-item
              clickable
              v-for="(opcao, letra) in opcoes"
              :key="letra"
              @click="responder(letra)"
            >
              <q-item-section>{{ letra }}) {{ opcao }}</q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <q-card v-if="resultado" class="q-mt-md">
        <q-card-section>
          <div :class="{ 'text-positive': resultado.acertou, 'text-negative': !resultado.acertou }">
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
import { useRoute, useRouter } from 'vue-router'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()

// Dados do item e chance
const item = ref(null)
const chance = ref(0)

// lista de habilidades (vinda do backend)
const habilidades = ref([])

// Animações
const mostrarBonk = ref(false)
const mostrarOvo = ref(false)

// Diálogo de perguntas
const mostrarDialogo = ref(false)
const questao = ref(null)
const resultado = ref(null)
const opcoes = ref({})

onMounted(async () => {
  const itemId = route.params.id
  if (itemId) {
    // busca item e progresso
    const [resItem, resCaptura] = await Promise.all([
      api.get(`/api/item/${itemId}/`),
      api.get(`/api/captura/${itemId}/`)
    ])
    item.value = resItem.data
    chance.value = resCaptura.data.chance

    // busca habilidades aplicáveis para este usuário e item
    try {
      const resHabs = await api.get(`/api/habilidades/${itemId}/habilidades/`)
      habilidades.value = resHabs.data
    } catch (err) {
      console.warn('Erro ao buscar habilidades', err)
      habilidades.value = []
    }
  }
})

/** Executa habilidade (chama backend) */
async function executarAcao(habilidade_id) {
  try {
    const itemId = route.params.id
    const res = await api.post(`/api/captura/${itemId}/`, { habilidade_id })
    if (res.data.chance !== undefined) chance.value = res.data.chance

    if (res.data.habilidade) {
      const h = res.data.habilidade
      const idx = habilidades.value.findIndex(x => x.id === h.id)
      if (idx !== -1) habilidades.value[idx] = { ...habilidades.value[idx], ...h }
    }
  } catch (err) {
    const msg = err?.response?.data?.detail || 'Erro ao executar ação'
    $q.notify({ type: 'negative', message: msg })
  }
}

/** Usa habilidade (Versão da MAIN) */
async function usarHabilidade(h) {
  if (h.quantidade === 0) {
    $q.notify({ type: 'negative', message: 'Sem usos restantes dessa habilidade.' })
    return
  }

  // tocar som se existir
  if (h.som) {
    const a = new Audio(h.som)
    a.play().catch(()=>{})
  }

  // animação customizada (se desejar)
  if (h.animacao) {
    // Exemplo: if (h.nome.toLowerCase().includes('ovo')) { mostrarOvo.value = true; setTimeout(()=>mostrarOvo.value=false,1000) }
  }

  await executarAcao(h.id)
}

/** Capturar (Versão do HEAD, com sua notificação melhorada) */
async function capturar() {
  // $q.loading.show({ message: 'Salvando na mochila...' }) 

  try {
    const itemId = route.params.id
    await api.post(`/api/captura/${itemId}/confirmar/`)
    chance.value = 100

    // Notificação de sucesso (SUA VERSÃO)
    $q.notify({
        type: 'positive',
        color: 'positive',
        icon: 'pets',
        message: `${item.value.nome} foi capturado e adicionado à mochila!`,
        position: 'top'
    })

    // $q.loading.hide() 
    router.push({ name: 'mapa' }) 
  
  } catch(err) {
    // $q.loading.hide() 
    console.error("Erro ao capturar:", err)
    $q.notify({ type: 'negative', message: 'Erro ao confirmar a captura' })
  }
}

/** Conversar */
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

/** Responder pergunta (Versão do HEAD, com sua lógica extra) */
async function responder(letra) {
  try {
    const res = await api.post(`/api/questao/${questao.value.id}/`, { resposta: letra })
    resultado.value = res.data

    // Sua lógica de executar ação ao acertar (SUA VERSÃO)
    if (res.data.acertou) {
      await executarAcao('conversar')
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
</script>

<style scoped>
.main-card {
  max-width: 700px;
  margin: auto;
  border-radius: 16px;
  padding: 16px;
  background-color: #ffffff; 
  display: flex;
  flex-direction: column;
}

.card-image { position: relative; max-height: 400px; }
.main-img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }

.bonk-animacao, .ovo-animacao {
  position:absolute; top:50%; left:50%;
  transform:translate(-50%,-50%);
  width:150px; pointer-events:none;
}
.fade-enter-active,.fade-leave-active { transition: opacity .5s; }
.fade-enter-from,.fade-leave-to { opacity:0; }

.actions-col { display:flex; flex-direction:column; gap:8px; align-items:center; justify-content:center; }

.progress-bar { position:relative; margin-top:12px; height:40px; }
.progress-text { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-weight:bold; color:rgb(119, 119, 119); }
.full-width { width:100%; }
</style>