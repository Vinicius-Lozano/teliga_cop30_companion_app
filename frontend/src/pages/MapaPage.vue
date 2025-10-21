<template>
  <q-page class="q-pa-md green-bg">
    <div class="q-pa-md flex flex-center">
      <q-card class="main-card">
        <q-card-section class="banner text-center">
          <h1>Te Liga!</h1>
          <p>Bem-vindo(a) ao mapa de eventos!</p>
        </q-card-section>

        <q-card-section>
          <q-no-ssr>
            <l-map
              v-if="isMounted"
              ref="mapRef"
              style="height: 70vh; width: 100%; border-radius: 1rem; overflow: hidden;"
              :zoom="13"
              :center="mapCenter"
            >
              <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
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
                    <br /><small>Clique no item para coletar</small>
                  </div>
                </l-popup>
              </l-marker>
            </l-map>
          </q-no-ssr>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
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

/*
  Agora: coletarPocao salva **no backend**.
  Rota esperada: POST /api/capturas/pocoes/  com { pocao_id: <id> }
  Se o backend usa outro nome de rota/payload, ajuste aqui.
*/
async function coletarPocao(pocao) {
  if (!pocao || !pocao.id) {
    $q.notify({ message: 'Poção inválida.', color: 'negative', position: 'top' })
    return
  }

  try {
    // tenta salvar no backend
    await api.post('/api/capturas/pocoes/', { pocao_id: pocao.id })

    // remove o item visível do mapa (coletado)
    itensAleatorios.value = itensAleatorios.value.filter(
      (item) => !(item.id === pocao.id && item.latitude === pocao.latitude)
    );

    $q.notify({
      message: `${pocao.nome} coletada e guardada na mochila!`,
      color: 'positive',
      icon: 'check_circle',
      position: 'top'
    });
  } catch (err) {
    const status = err?.response?.status
    if (status === 400 || status === 409) {
      $q.notify({
        message: `${pocao.nome} já foi coletada.`,
        color: 'info',
        icon: 'info',
        position: 'top'
      });
    } else if (status === 401) {
      $q.notify({
        message: 'Você precisa estar logado para coletar poções.',
        color: 'warning',
        position: 'top'
      });
      // opcional: redirecionar para login
      // router.push('/login')
    } else {
      console.error('Erro ao coletar poção:', err)
      $q.notify({
        message: 'Erro ao coletar poção. Tente novamente.',
        color: 'negative',
        position: 'top'
      });
    }
  }
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

.main-card {
  width: 100%;
  max-width: 1000px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.banner {
  background: linear-gradient(90deg, #2e7d32, #43a047);
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
  padding: 2rem 1rem;
  border-bottom: 4px solid #66bb6a;
}

.banner h1 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
  letter-spacing: 1px;
}

.banner p {
  font-size: 1.2rem;
  opacity: 0.95;
  margin: 0;
}

/* POPUPS DO MAPA */
.leaflet-popup-content-wrapper {
  background: white;
  color: #333;
  font-size: 0.95rem;
  border-radius: 10px;
}

.leaflet-popup-tip {
  background: white;
}

b {
  color: #2e7d32;
  font-weight: 600;
}
small {
  color: #777;
  font-size: 0.8rem;
}
</style>
