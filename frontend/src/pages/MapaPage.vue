<template>
  <div>
    <!-- Banner -->
    <header class="banner">
      <h1>Te Liga!</h1>
      <p>Bem-vindo(a) ao mapa de eventos!</p>
    </header>

    <!-- Mapa -->
    <q-no-ssr>
      <l-map
        v-if="isMounted"
        ref="mapRef"
        style="height: 80vh; width: 100%;"
        :zoom="13"
        :center="mapCenter"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        <!-- Marker do usuário -->
        <l-marker
          v-if="usuarioPos"
          :lat-lng="usuarioPos"
          :icon="usuarioIcon"
          :popup="'Você está aqui'"
        />

        <!-- Markers de eventos (somente com coordenadas válidas) -->
        <l-marker
          v-for="evento in eventosValidos"
          :key="evento.id"
          :lat-lng="[evento.latitude, evento.longitude]"
          @click="irParaDetalhes(evento.id)"
          :popup="evento.nome"
        />

        <!-- Markers de itens próximos (somente com coordenadas válidas) -->
        <l-marker
          v-for="item in itensProximosValidos"
          :key="item.id"
          :lat-lng="[item.latitude, item.longitude]"
          :icon="getIcon(item.tipo)"
          @click="irParaDetalhesItem(item.id)"
        />
      </l-map>
    </q-no-ssr>
  </div>
</template>

<script setup>
defineOptions({ name: 'MapaPage' })

import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Corrige ícones padrão do Leaflet
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import shadowUrl from 'leaflet/dist/images/marker-shadow.png'
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png'
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl })

const router = useRouter()
const isMounted = ref(false)
const mapRef = ref(null)
const mapCenter = ref([-1.4558, -48.4902]) // Centro inicial
const usuarioPos = ref(null)
const eventos = ref([])
const itensProximos = ref([])

function getIcon(tipo) {
  const largura = 40;
  const altura = 40;
  const anchor = [largura / 2, altura];

  switch (tipo) {
    case 'ANI':
      return L.icon({
        iconUrl: '/icons/animal.png',
        iconSize: [largura, altura],
        iconAnchor: anchor
      })
    case 'PLA':
      return L.icon({
        iconUrl: '/icons/planta.png',
        iconSize: [largura, altura],
        iconAnchor: anchor
      })
    default:
      return L.icon({
        iconUrl: '/icons/item_padrao.png',
        iconSize: [largura, altura],
        iconAnchor: anchor
      })
  }
}

// Ícone do usuário (use PNG com fundo transparente)
const usuarioIcon = L.icon({
  iconUrl: '/icons/usuario.png', // coloque um PNG transparente em /public/icons/
  iconSize: [40, 40],
  iconAnchor: [20, 40]
})

// Funções de navegação
function irParaDetalhes(id) {
  router.push(`/details/${id}`)
}
function irParaDetalhesItem(id) {
  router.push(`/item/${id}`)
}

// Computed para filtrar eventos válidos
const eventosValidos = computed(() => eventos.value.filter(e => e.latitude != null && e.longitude != null))
const itensProximosValidos = computed(() => itensProximos.value.filter(i => i.latitude != null && i.longitude != null))

// Obter posição do usuário e centralizar o mapa
async function obterPosicaoUsuario() {
  if (!navigator.geolocation) { 
    alert('Seu navegador não suporta geolocalização!'); 
    return 
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      usuarioPos.value = [position.coords.latitude, position.coords.longitude]
      mapCenter.value = usuarioPos.value
      if (mapRef.value?.mapObject) mapRef.value.mapObject.setView(usuarioPos.value, 13)

      await carregarItensProximos()
    },
    (err) => console.error('Erro ao obter localização:', err)
  )
}

async function carregarItensProximos() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}api/itens_proximos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        latitude: usuarioPos.value[0],
        longitude: usuarioPos.value[1],
        qtd_itens: 10
      })
    })
    itensProximos.value = await response.json()
  } catch (err) {
    console.error('Erro ao carregar itens próximos:', err)
  }
}


onMounted(async () => {
  isMounted.value = true
  obterPosicaoUsuario() 
  try {
    const eventosResponse = await fetch(`${import.meta.env.VITE_API_URL}api/eventos/`)
    eventos.value = await eventosResponse.json()
  } catch (err) {
    console.error('Erro ao carregar eventos:', err)
  }
})

</script>

<style scoped>
.banner {
  background-color: #2e7d32;
  color: white;
  text-align: center;
  padding: 2rem 1rem;
}
.banner h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
.banner p { font-size: 1.2rem; margin: 0; }
</style>
