<template>
  <q-page class="container">
    <!-- Botão de voltar -->
    <div class="row justify-end q-mb-md">
      <q-btn label="Voltar para o mapa" flat icon="arrow_back" @click="$router.push('/')" />
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
          </div>
        </div>
      </div>

      <!-- Curiosidades e imagens extras (opcional) -->
      <div v-if="item.curiosidades || item.imagensExtras?.length" class="card q-pa-lg q-mb-xl">
        <div class="section-title">
          <q-icon name="emoji_objects" color="amber-8" />
          Curiosidades
        </div>
        <div v-if="item.curiosidades" class="text-body1 q-mb-lg" style="color:#374151; line-height:1.7">
          {{ item.curiosidades }}
        </div>
        <div v-if="item.imagensExtras?.length" class="thumb-strip">
          <img v-for="(img, i) in item.imagensExtras" :key="i" :src="img" class="thumb" />
        </div>
      </div>

      <!-- Localização no mapa -->
      <div class="card q-pa-lg q-mb-xl">
        <div class="section-title">
          <q-icon name="public" color="green-8" />
          Localização no mapa
        </div>
        <div id="map" class="map q-mb-md" style="height: 300px;"></div>
        <div class="text-body1" style="color:#374151">
          📍 <b>{{ item.endereco || 'Coordenadas não disponíveis' }}</b><br />
          📅 Coletado em <i>{{ item.data || 'Não informado' }}</i>
        </div>
      </div>
    </div>

    <!-- Caso item não encontrado -->
    <div v-else class="text-center q-mt-xl">
      <q-icon name="error_outline" color="red" size="64px" />
      <div class="text-h6 q-mt-md">Item não encontrado</div>
      <q-btn color="primary" label="Voltar para o mapa" class="q-mt-lg" @click="$router.push('/')" />
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const item = ref(null)

// Função para escolher o ícone de acordo com o tipo
function getIconUrl(tipo) {
  switch(tipo) {
    case 'ANI': return '/icons/animal.png'
    case 'PLA': return '/icons/planta.png'
    default: return '/icons/item_padrao.png'
  }
}

onMounted(async () => {
  try {
    // Busca os dados do item
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/item/${route.params.id}/`)
    item.value = await response.json()

    // Inicializa o mapa apenas se houver coordenadas válidas
    if (item.value?.latitude != null && item.value?.longitude != null) {
      await nextTick()

      const map = L.map('map').setView([item.value.latitude, item.value.longitude], 15)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map)

      const icon = L.icon({
        iconUrl: getIconUrl(item.value.tipo),
        iconSize: [40, 40],
        iconAnchor: [20, 40]
      })

      L.marker([item.value.latitude, item.value.longitude], { icon })
        .addTo(map)
        .bindPopup(`<b>${item.value.nome}</b>`)
    }
  } catch (err) {
    console.error('Erro ao carregar item:', err)
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
