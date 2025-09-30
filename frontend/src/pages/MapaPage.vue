<template>
  <div>
    <header class="banner">
      <h1>Te Liga!</h1>
      <p>Bem-vindo(a) ao mapa de eventos!</p>
    </header>

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

        <l-marker
          v-if="usuarioPos"
          :lat-lng="usuarioPos"
          :icon="usuarioIcon"
        >
          <l-popup>Você está aqui</l-popup>
        </l-marker>

        <l-marker
          v-for="evento in eventosFixosValidos"
          :key="`evento-${evento.id}`"
          :lat-lng="[evento.latitude, evento.longitude]"
          @click="irParaDetalhesEvento(evento.id)"
        >
          <l-popup>{{ evento.titulo }}</l-popup>
        </l-marker>

        <l-marker
          v-for="item in itensAleatoriosValidos"
          :key="`item-${item.id}-${item.latitude}`"
          :lat-lng="[item.latitude, item.longitude]"
          :icon="getIcon(item.tipo)"
          @click="handleItemClick(item)"
        >
          <l-popup>
            <b>{{ item.nome }}</b>
            <div v-if="item.tipo === 'POC'">
              Bônus de Captura: +{{ item.bonus_captura }}%
              <br><small>Clique no item para coletar</small>
            </div>
          </l-popup>
        </l-marker>
      </l-map>
    </q-no-ssr>
  </div>
</template>

<script setup>
defineOptions({ name: 'MapaPage' })

import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

// Corrige ícones padrão do Leaflet
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import shadowUrl from 'leaflet/dist/images/marker-shadow.png'
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png'
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl })

const router = useRouter()
const $q = useQuasar()
const isMounted = ref(false)
const mapRef = ref(null)
const mapCenter = ref([-1.4558, -48.4902])
const usuarioPos = ref(null)

const eventosFixos = ref([])
const itensAleatorios = ref([])

function getIcon(tipo) {
  const largura = 40;
  const altura = 40;
  const anchor = [largura / 2, altura];
  let url = '/icons/item_padrao.png';
  if (tipo === 'ANI') url = '/icons/animal.png';
  if (tipo === 'PLA') url = '/icons/planta.png';
  if (tipo === 'POC') url = '/icons/potion.svg'; 
  return L.icon({ iconUrl: url, iconSize: [largura, altura], iconAnchor: anchor });
}

const usuarioIcon = L.icon({
  iconUrl: '/icons/usuario.png',
  iconSize: [40, 40],
  iconAnchor: [20, 40]
})

function irParaDetalhesEvento(id) {
  router.push(`/details/${id}`)
}


function coletarPocao(pocao) {
  const mochila = JSON.parse(localStorage.getItem("mochila")) || [];
  mochila.push({ ...pocao, tipoConteudo: "item" });
  localStorage.setItem("mochila", JSON.stringify(mochila));

  itensAleatorios.value = itensAleatorios.value.filter(
    (item) => !(item.id === pocao.id && item.latitude === pocao.latitude)
  );

  $q.notify({
    message: `${pocao.nome} coletada e guardada na mochila!`,
    color: 'positive',
    icon: 'check_circle',
    position: 'top'
  });
}

function handleItemClick(item) {
  if (item.tipo === 'POC') {
    coletarPocao(item);
  } else {
    router.push(`/item/${item.id}?lat=${item.latitude}&lon=${item.longitude}`);
  }
}

const eventosFixosValidos = computed(() => eventosFixos.value.filter(e => e.latitude != null && e.longitude != null))
const itensAleatoriosValidos = computed(() => itensAleatorios.value.filter(i => i.latitude != null && i.longitude != null))

async function obterPosicaoUsuario() {
  if (!navigator.geolocation) return;
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
  if (!usuarioPos.value) return;
  try {
    const response = await api.post('/api/itens_proximos/', {
        latitude: usuarioPos.value[0],
        longitude: usuarioPos.value[1],
        qtd_itens: 10
    })
    itensAleatorios.value = response.data;
  } catch (err) {
    console.error('Erro ao carregar itens próximos:', err)
  }
}

async function carregarEventosFixos() {
  try {
    const response = await api.get('/api/events/')
    eventosFixos.value = response.data
  } catch (err)
{
    console.error('Erro ao carregar eventos fixos:', err)
  }
}

onMounted(async () => {
  isMounted.value = true
  obterPosicaoUsuario()
  await carregarEventosFixos();
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