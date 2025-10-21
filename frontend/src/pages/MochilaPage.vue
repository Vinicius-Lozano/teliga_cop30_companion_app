<template>
  <q-page class="q-pa-md flex flex-center">

    <!-- CARD PRINCIPAL BRANCO -->
    <q-card class="main-card q-pa-lg q-ma-md">

      <!-- Cabeçalho -->
      <div class="row items-center q-mb-lg">
        <q-btn flat round dense icon="arrow_back" color="primary" @click="$router.back()" />
        <div class="text-h5 text-primary text-weight-bold q-ml-md">
          🎒 Minha Mochila
        </div>
      </div>

      <div class="text-subtitle1 text-grey-8 q-mb-xl">
        Aqui ficam os itens, poções e eventos que você capturou.
      </div>

      <!-- ITENS -->
      <div class="q-mb-xl">
        <div class="row items-center q-mb-sm">
          <q-icon name="inventory_2" size="sm" class="q-mr-sm text-amber-8" />
          <div class="text-h6 text-amber-9 text-weight-bold">Itens</div>
        </div>
        <q-separator color="amber-5" />

        <div v-if="itens.length === 0" class="text-grey-7 text-italic q-mt-md">
          Você ainda não capturou nenhum item.
        </div>

        <div class="q-mt-md grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <q-card
            v-for="item in itens"
            :key="item.id"
            flat
            bordered
            class="q-pa-md hover-card"
          >
            <q-card-section>
              <div class="text-h6 text-amber-9">{{ item.nome }}</div>
              <div class="text-body1 text-grey-8">{{ item.descricao }}</div>
              <div
                v-if="item.tipo === 'POC'"
                class="text-positive text-weight-bold q-mt-sm"
              >
                Bônus de Captura: +{{ item.bonus_captura }}%
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- POÇÕES -->
      <div class="q-mb-xl">
        <div class="row items-center q-mb-sm">
          <q-icon name="science" size="sm" class="q-mr-sm text-light-blue-8" />
          <div class="text-h6 text-light-blue-9 text-weight-bold">Poções</div>
        </div>
        <q-separator color="light-blue-5" />

        <div v-if="pocoes.length === 0" class="text-grey-7 text-italic q-mt-md">
          Você ainda não possui nenhuma poção.
        </div>

        <div class="q-mt-md grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <q-card
            v-for="pocao in pocoes"
            :key="pocao.id"
            flat
            bordered
            class="q-pa-md hover-card"
          >
            <q-card-section>
              <div class="text-h6 text-light-blue-9">{{ pocao.nome }}</div>
              <div class="text-body1 text-grey-8">{{ pocao.descricao }}</div>
              <div
                v-if="pocao.chance_bonus"
                class="text-blue-9 text-weight-bold q-mt-sm"
              >
                💫 Chance de Captura: {{ pocao.chance_bonus }}%
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- EVENTOS -->
      <div class="q-mb-xl">
        <div class="row items-center q-mb-sm">
          <q-icon name="event" size="sm" class="q-mr-sm text-deep-purple-6" />
          <div class="text-h6 text-deep-purple-8 text-weight-bold">Eventos</div>
        </div>
        <q-separator color="deep-purple-5" />

        <div v-if="eventos.length === 0" class="text-grey-7 text-italic q-mt-md">
          Você ainda não capturou nenhum evento.
        </div>

        <div class="q-mt-md grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <q-card
            v-for="evento in eventos"
            :key="evento.id"
            flat
            bordered
            class="q-pa-md hover-card relative-position cursor-pointer"
            @click="verDetalhesEvento(evento)"
          >
            <q-card-section>
              <div class="row items-center justify-between">
                <div class="text-h6 text-deep-purple-8">{{ evento.titulo }}</div>
                <q-btn
                  dense
                  flat
                  round
                  icon="delete"
                  color="negative"
                  size="sm"
                  @click.stop="confirmarRemocao(evento)"
                />
              </div>
              <div class="text-body1 text-grey-8">
                Categoria: {{ evento.categoria }}
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- DIÁLOGO -->
      <q-dialog v-model="dialogAberto" persistent>
        <q-card>
          <q-card-section class="row items-center">
            <q-icon name="warning" color="warning" size="md" class="q-mr-sm" />
            <div class="text-h6">Remover evento</div>
          </q-card-section>

          <q-card-section>
            Tem certeza que deseja remover o evento
            <b>{{ eventoSelecionado?.titulo }}</b> da mochila?
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" color="grey" v-close-popup />
            <q-btn flat label="Remover" color="negative" @click="removerEventoConfirmado" />
          </q-card-actions>
        </q-card>
      </q-dialog>

    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useQuasar } from "quasar"
import { api } from "boot/axios"

const router = useRouter()
const $q = useQuasar()

const itens = ref([])
const pocoes = ref([])
const eventos = ref([])
const dialogAberto = ref(false)
const eventoSelecionado = ref(null)

onMounted(async () => {
  try {
    const resItens = await api.get("/api/capturas/items/")
    itens.value = resItens.data
      .map((i) => ({
        id: i.item.id,
        nome: i.item.nome,
        descricao: i.item.descricao,
        bonus_captura: i.item.bonus_captura,
        tipo: i.item.tipo
      }))
      .filter((i) => !i.nome.toLowerCase().includes("poção"))

    const resPocoes = await api.get("/api/capturas/pocoes/")
    pocoes.value = resPocoes.data.map((p) => ({
      id: p.item.id,
      nome: p.item.nome,
      descricao: p.item.descricao,
      chance_bonus: p.chance_bonus || p.item.bonus_captura || 0
    }))

    const resEventos = await api.get("/api/capturas/eventos/")
    eventos.value = resEventos.data.map((e) => ({
      id: e.evento.id,
      titulo: e.evento.titulo,
      categoria: e.evento.categoria
    }))
  } catch (err) {
    console.error(err)
    $q.notify({ type: "negative", message: "Erro ao carregar mochila" })
  }
})

function verDetalhesEvento(evento) {
  router.push(`/details/${evento.id}`)
}

function confirmarRemocao(evento) {
  eventoSelecionado.value = evento
  dialogAberto.value = true
}

async function removerEventoConfirmado() {
  if (!eventoSelecionado.value) return
  try {
    const eventoId = eventoSelecionado.value.id
    await api.delete(`/api/capturas/eventos/${eventoId}/`)
    eventos.value = eventos.value.filter((e) => e.id !== eventoId)
    $q.notify({ type: "positive", message: "Evento removido com sucesso!" })
  } catch (error) {
    console.error("Erro ao remover evento:", error)
    $q.notify({ type: "negative", message: "Não foi possível remover o evento." })
  } finally {
    dialogAberto.value = false
    eventoSelecionado.value = null
  }
}
</script>

<style scoped>
.main-card {
  max-width: 1100px;
  width: 100%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.hover-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}
.cursor-pointer {
  cursor: pointer;
}

/* Tipografia mais legível */
.text-h5 {
  font-size: 1.7rem;
}
.text-h6 {
  font-size: 1.3rem;
}
.text-body1 {
  font-size: 1.1rem;
}
</style>
