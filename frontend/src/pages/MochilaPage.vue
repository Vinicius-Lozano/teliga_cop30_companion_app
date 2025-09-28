<template>
  <q-page class="q-pa-md">

    <div class="row items-center q-mb-lg">
      <q-btn flat round dense icon="arrow_back" @click="$router.back()" />
      <div class="text-h5 q-ml-md">🎒 Minha Mochila</div>
    </div>

    <div class="text-subtitle1 text-grey-7 q-mb-xl">
      Aqui ficam os itens e eventos que você capturou.
    </div>

    <div class="q-mb-xl">
      <div class="row items-center q-mb-sm">
        <q-icon name="inventory_2" size="sm" class="q-mr-sm text-primary" />
        <div class="text-h6">Itens</div>
      </div>
      <q-separator />

      <div v-if="itens.length === 0" class="text-grey text-italic q-mt-md">
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
            <div class="text-subtitle1 text-primary">{{ item.nome }}</div>
            <div class="text-caption text-grey-7">{{ item.descricao }}</div>
            <div v-if="item.tipo === 'POC'" class="text-positive text-weight-bold q-mt-sm">
              Bônus de Captura: +{{ item.bonus_captura }}%
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <div class="q-mb-xl">
      <div class="row items-center q-mb-sm">
        <q-icon name="event" size="sm" class="q-mr-sm text-secondary" />
        <div class="text-h6">Eventos</div>
      </div>
      <q-separator />

      <div v-if="eventos.length === 0" class="text-grey text-italic q-mt-md">
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
              <div class="text-subtitle1 text-secondary">{{ evento.titulo }}</div>
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
            <div class="text-caption text-grey-7">
              Categoria: {{ evento.categoria }}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

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

  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { useRouter } from 'vue-router'

const router = useRouter()
const mochila = ref([])
const dialogAberto = ref(false)
const eventoSelecionado = ref(null)

onMounted(() => {
  mochila.value = JSON.parse(localStorage.getItem("mochila")) || []
})

const itens = computed(() =>
  mochila.value.filter((m) => m.tipoConteudo === "item")
)

const eventos = computed(() =>
  mochila.value.filter((m) => m.tipoConteudo === "evento")
)

function verDetalhesEvento(evento) {
  router.push(`/details/${evento.id}`)
}

function confirmarRemocao(evento) {
  eventoSelecionado.value = evento
  dialogAberto.value = true
}

function removerEventoConfirmado() {
  if (eventoSelecionado.value) {
    mochila.value = mochila.value.filter(
      (m) => !(m.tipoConteudo === "evento" && m.id === eventoSelecionado.value.id)
    )
    localStorage.setItem("mochila", JSON.stringify(mochila.value))
  }
  dialogAberto.value = false
  eventoSelecionado.value = null
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}
.cursor-pointer {
  cursor: pointer;
}
</style>