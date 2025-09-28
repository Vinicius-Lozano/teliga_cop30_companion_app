<template>
  <q-page class="container q-pa-md">
    <!-- Botão de voltar -->
    <div class="row justify-end q-mb-md">
      <q-btn label="Voltar para o mapa" flat icon="arrow_back" to="/" />
    </div>

    <!-- Detalhes do item -->
    <div v-if="item">
      <div class="card q-pa-md q-mb-xl">
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-6">
            <q-img :src="item.imagem" style="width:100%; height:300px" class="rounded-borders" />
          </div>
          <div class="col-12 col-md-6">
            <h1 class="q-mt-none q-mb-sm" style="color:#166534; font-size:36px; font-weight:900; line-height:1.1">
              {{ item.nome }}
            </h1>
            <span class="subtitle-chip q-mb-md">{{ item.tipo }}</span>
            <div class="text-body1 q-mt-md" style="color:#374151; line-height:1.7">
              {{ item.descricao }}
            </div>

            <!-- Botão para guardar na mochila -->
            <q-btn 
              color="green-8" 
              icon="backpack" 
              label="Guardar na Mochila" 
              class="q-mt-lg"
              @click="guardarNaMochila" 
            />
          </div>
        </div>
      </div>

      <!-- Curiosidades -->
      <div v-if="item.curiosidades" class="card q-pa-lg q-mb-xl">
        <div class="section-title">
          <q-icon name="emoji_objects" color="amber-8" />
          Curiosidades
        </div>
        <div class="text-body1 q-mb-lg" style="color:#374151; line-height:1.7">
          {{ item.curiosidades }}
        </div>
      </div>

      <!-- Localização no mapa -->
      <div class="card q-pa-lg q-mb-xl">
        <div class="section-title">
          <q-icon name="public" color="green-8" />
          Localização no mapa
        </div>
        <div id="map" class="map q-mb-md" style="height: 300px;"></div>
      </div>
    </div>

    <!-- Caso item não encontrado -->
    <div v-else class="text-center q-mt-xl">
      <q-spinner color="primary" size="3em" v-if="isLoading" />
      <div v-else>
        <q-icon name="error_outline" color="red" size="64px" />
        <div class="text-h6 q-mt-md">Item não encontrado</div>
        <q-btn color="primary" label="Voltar para o mapa" class="q-mt-lg" to="/" />
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { api } from 'boot/axios'

const route = useRoute()
const item = ref(null)
const isLoading = ref(true)
const $q = useQuasar()

// Função para escolher o ícone de acordo com o tipo
function getIconUrl(tipo) {
  switch(tipo) {
    case 'ANI': return '/icons/animal.png'
    case 'PLA': return '/icons/planta.png'
    default: return '/icons/item_padrao.png'
  }
}

// Função para guardar o item na mochila 
function guardarNaMochila() {
  let mochila = JSON.parse(localStorage.getItem('mochila')) || []
  if (!mochila.find(i => i.id === item.value.id && i.tipoConteudo === 'item')) {
    mochila.push({ ...item.value, tipoConteudo: 'item' })
    localStorage.setItem('mochila', JSON.stringify(mochila))
    $q.notify({ type: 'positive', message: `${item.value.nome} foi guardado na mochila!` })
  } else {
    $q.notify({ type: 'info', message: `${item.value.nome} já está na mochila!` })
  }
}

onMounted(async () => {
  try {
    // 1. Busca os detalhes do item (descrição, nome, etc.)
    const response = await api.get(`/api/item/${route.params.id}/`)
    item.value = response.data

    // 2. Pega as coordenadas da URL
    const lat = route.query.lat;
    const lon = route.query.lon;

    // 3. Inicializa o mapa APENAS se houver coordenadas na URL
    if (lat != null && lon != null) {
      await nextTick()

      const latitude = parseFloat(lat);
      const longitude = parseFloat(lon);

      const map = L.map('map').setView([latitude, longitude], 16) 
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map)

      const icon = L.icon({
        iconUrl: getIconUrl(item.value.tipo),
        iconSize: [40, 40],
        iconAnchor: [20, 40]
      })

      L.marker([latitude, longitude], { icon })
        .addTo(map)
        .bindPopup(`<b>${item.value.nome}</b>`)
        .openPopup(); 
    }
  } catch (err) {
    console.error('Erro ao carregar item:', err)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.map {
  width: 100%;
}
.thumb-strip {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
}
.thumb {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}
</style>
