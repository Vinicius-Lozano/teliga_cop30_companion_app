<template>
  <q-page class="green-landing">
    <div class="parallax" aria-hidden="true">
      <div class="clouds">
        <span class="cloud" style="--t:12%; --speed:60s;  --scale:1.05; --delay:-30s;"></span>
        <span class="cloud" style="--t:22%; --speed:80s;  --scale:0.95; --delay:-10s;"></span>
        <span class="cloud" style="--t:33%; --speed:70s;  --scale:1.00; --delay:-50s;"></span>
        <span class="cloud" style="--t:18%; --speed:90s;  --scale:1.10; --delay:-70s;"></span>
        <span class="cloud" style="--t:28%; --speed:110s; --scale:1.18; --delay:-90s;"></span>
        <span class="cloud" style="--t:8%;  --speed:75s;  --scale:0.85; --delay:-20s;"></span>
      </div>
      <div class="mountains far"></div>
      <div class="mountains near"></div>
    </div>

    <section class="hero">
      <div class="hero-inner">
        <div class="phone-col">
          <div class="phone-frame">
            <div class="notch"></div>

            <q-no-ssr>
              <l-map
                v-if="isMounted"
                ref="mapRef"
                class="map-hero"
                :zoom="13"
                :center="mapCenter"
                :zoomControl="false"
                :scrollWheelZoom="false"
                :doubleClickZoom="false"
                :dragging="true"
              >
                <l-tile-layer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                />

                <l-marker v-if="usuarioPos" :lat-lng="usuarioPos" :icon="usuarioIcon">
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

            <div class="play-pill" @click="router.push(PLAY_ROUTE)">JOGAR</div>
          </div>
        </div>

        <div class="copy-col">
          <div class="brand-badge">
            <span class="pin">📍</span><strong>TE LIGA!</strong>
          </div>

          <h1 class="title">
            Descubra o<br />
            <span>Turismo de Forma Gamificada</span>
          </h1>

          <p class="subtitle">
            Lorem ipsum dolor sit amet. Eum consectetur minima et expedita nisi non pariatur maxime et autem minus rem atque iste et ducimus voluptas? Aut quia aliquam qui repudiandae ducimus et dignissimos nobis ad sapiente dolores ut consequatur quis aut optio amet id fuga nobis. Vel dolor illo et omnis voluptatum qui Quis nihil sed possimus sint id quas officiis eos vitae accusantium. Et dolorem nihil eum commodi neque quo vero consequatur est nihil iure.
          </p>

          <div class="cta-row">
            <q-btn class="cta primary" unelevated rounded size="lg" @click="scrollTo('#sobre')">
              Conheça o Projeto
            </q-btn>
            <q-btn class="cta ghost" rounded size="lg" @click="router.push(CTA_ROUTE)">
              Criar Conta
            </q-btn>
          </div>
        </div>
      </div>
    </section>

    <section id="sobre" class="about">
      <div class="about-card">
        <div class="about-illu" aria-hidden="true">🏙️</div>
        <div class="about-text">
          <h2>Sobre o Projeto</h2>
          <p>
            Lorem ipsum dolor sit amet. Eum consectetur minima et expedita nisi non pariatur maxime et autem minus rem atque iste et ducimus voluptas? Aut quia aliquam qui repudiandae ducimus et dignissimos nobis ad sapiente dolores ut consequatur quis aut optio amet id fuga nobis. Vel dolor illo et omnis voluptatum qui Quis nihil sed possimus sint id quas officiis eos vitae accusantium. Et dolorem nihil eum commodi neque quo vero consequatur est nihil iure.
          </p>
        </div>
      </div>
    </section>

    <section id="como-funciona" class="how">
      <h2>Como Funciona</h2>
      <div class="how-grid">
        <div class="how-card">
          <div class="how-icon">📍</div>
          <h3>Explore Locais</h3>
          <p>Descubra pontos de interesse e eventos próximos a você.</p>
        </div>
        <div class="how-card">
          <div class="how-icon">🎮</div>
          <h3>Colete <br> Pontos</h3>
          <p>Ganhe pontos ao visitar locais e coletar itens no mapa.</p>
        </div>
        <div class="how-card">
          <div class="how-icon">🏆</div>
          <h3>Ganhe Recompensas</h3>
          <p>Troque seus pontos por benefícios e conquistas no app.</p>
        </div>
      </div>
    </section>
  </q-page>
</template>

<script setup>
defineOptions({ name: 'LandingTeLiga' })

import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const CTA_ROUTE = '/register'
const PLAY_ROUTE = '/'

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

function getIcon (tipo) {
  const largura = 40, altura = 40
  const anchor = [largura / 2, altura]
  let url = '/icons/item_padrao.png'
  if (tipo === 'ANI') url = '/icons/animal.png'
  if (tipo === 'PLA') url = '/icons/planta.png'
  if (tipo === 'POC') url = '/icons/potion.svg'
  return L.icon({ iconUrl: url, iconSize: [largura, altura], iconAnchor: anchor })
}

const usuarioIcon = L.icon({ iconUrl: '/icons/usuario.png', iconSize: [40, 40], iconAnchor: [20, 40] })

function irParaDetalhesEvento (id) { router.push(`/details/${id}`) }

async function coletarPocao (pocao) {
  if (!pocao?.id) return $q.notify({ message: 'Poção inválida.', color: 'negative', position: 'top' })
  try {
    await api.post('/api/capturas/pocoes/', { pocao_id: pocao.id })
    itensAleatorios.value = itensAleatorios.value.filter(
      (item) => !(item.id === pocao.id && item.latitude === pocao.latitude)
    )
    $q.notify({ message: `${pocao.nome} coletada e guardada na mochila!`, color: 'positive', icon: 'check_circle', position: 'top' })
  } catch (err) {
    const status = err?.response?.status
    if (status === 400 || status === 409) $q.notify({ message: `${pocao.nome} já foi coletada.`, color: 'info', icon: 'info', position: 'top' })
    else if (status === 401) $q.notify({ message: 'Você precisa estar logado para coletar poções.', color: 'warning', position: 'top' })
    else { console.error('Erro ao coletar poção:', err); $q.notify({ message: 'Erro ao coletar poção. Tente novamente.', color: 'negative', position: 'top' }) }
  }
}

function handleItemClick (item) {
  if (item.tipo === 'POC') coletarPocao(item)
  else router.push(`/item/${item.id}?lat=${item.latitude}&lon=${item.longitude}`)
}

const eventosFixosValidos = computed(() => eventosFixos.value.filter(e => e.latitude != null && e.longitude != null))
const itensAleatoriosValidos = computed(() => itensAleatorios.value.filter(i => i.latitude != null && i.longitude != null))

async function obterPosicaoUsuario () {
  if (!navigator.geolocation) return
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      usuarioPos.value = [pos.coords.latitude, pos.coords.longitude]
      mapCenter.value = usuarioPos.value
      if (mapRef.value?.mapObject) mapRef.value.mapObject.setView(usuarioPos.value, 13)
      await carregarItensProximos()
    },
    (err) => console.error('Erro ao obter localização:', err)
  )
}

async function carregarItensProximos () {
  if (!usuarioPos.value) return
  try {
    const { data } = await api.post('/api/itens_proximos/', {
      latitude: usuarioPos.value[0], longitude: usuarioPos.value[1], qtd_itens: 10
    })
    itensAleatorios.value = data
  } catch (err) { console.error('Erro ao carregar itens próximos:', err) }
}

async function carregarEventosFixos () {
  try { const { data } = await api.get('/api/events/'); eventosFixos.value = data }
  catch (err) { console.error('Erro ao carregar eventos fixos:', err) }
}

function scrollTo (selector) {
  const el = document.querySelector(selector)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(async () => {
  isMounted.value = true
  obterPosicaoUsuario()
  await carregarEventosFixos()
})
</script>

<style scoped>
.green-landing{
  --green-700:#2e7d32; --green-600:#43a047; --green-500:#66bb6a;
  --sky-400:#53a7ff; --sky-300:#6fd0ff;
  --bg:linear-gradient(180deg,var(--sky-400) 0%,var(--sky-300) 45%,#eafff0 100%);
  min-height:100vh; background:var(--bg); position:relative; overflow-x:hidden; color:#0a1b0d;
}

.parallax{ position:absolute; inset:0; z-index:0; overflow:hidden; pointer-events:none; }

.clouds{ position:absolute; left:0; right:0; top:0; height:55vh; }
.cloud{
  position:absolute; left:-30vw; top:var(--t,20%);
  width:240px; height:82px; border-radius:50px;
  background: rgba(255,255,255,.92);
  box-shadow:
    -60px 10px 0 10px rgba(255,255,255,.92),
    -20px -6px 0  8px rgba(255,255,255,.92),
     40px  0px 0 10px rgba(255,255,255,.92),
     80px 10px 0  8px rgba(255,255,255,.92);
  filter: blur(0.5px);
  opacity:.78;
  transform: translateX(-30vw) scale(var(--scale,1));
  animation: cloud-drift var(--speed,80s) linear infinite;
  animation-delay: var(--delay,-40s); /* já entra visível */
}
@keyframes cloud-drift{
  0%   { transform: translateX(-30vw) scale(var(--scale,1)); }
  100% { transform: translateX(130vw) scale(var(--scale,1)); }
}

.mountains{
  position:absolute; left:0; right:0; bottom:0;
  pointer-events:none; will-change: background-position;
}

.mountains.far{
  height:26vh; opacity:.96;
  background-image:
    linear-gradient(to top, rgba(255,255,255,.03), rgba(255,255,255,0) 45%),
    /* tile com 2 copas por bloco */
    radial-gradient(80px 80px at 40px 100%,  #0b5a39 79px, transparent 80px),
    radial-gradient(68px 68px at 120px 100%, #0b5a39 67px, transparent 68px);
  background-size:
    100% 100%,   /* haze */
    160px 100%,  /* copa A */
    160px 100%;  /* copa B */
  background-repeat: no-repeat, repeat-x, repeat-x;
  background-position:
    0 0,
    0 100%,
    0 100%;
  animation: forest-far 70s linear infinite;
  filter: saturate(.95);
}

.mountains.near{
  height:23vh; bottom:-1vh; opacity:1;
  background-image:
    linear-gradient(to top, rgba(255,255,255,.06), rgba(255,255,255,0) 45%),
    radial-gradient(100px 100px at 60px 100%,  #0a6e46 99px, transparent 100px),
    radial-gradient(90px  90px  at 160px 100%, #0a6e46 89px, transparent 90px);
  background-size:
    100% 100%,
    200px 100%,
    200px 100%;
  background-repeat: no-repeat, repeat-x, repeat-x;
  background-position:
    0 0,
    0 100%,
    0 100%;
  animation: forest-near 38s linear infinite;
  filter: drop-shadow(0 -6px 18px rgba(0,0,0,.12));
}

@keyframes forest-far  { 0% {background-position:0 0,    0 100%,    0 100%} 100% {background-position:0 0,   -160px 100%, -160px 100%} }
@keyframes forest-near { 0% {background-position:0 0,    0 100%,    0 100%} 100% {background-position:0 0,   -200px 100%, -200px 100%} }

@media (prefers-reduced-motion: reduce){
  .cloud, .mountains.far, .mountains.near { animation: none !important; }
}

.hero{ position:relative; z-index:1; }
.hero-inner{
  max-width:1200px; margin:0 auto; padding:48px 20px 24px;
  display:grid; grid-template-columns:1.1fr 1fr; gap:28px;
  align-items: center; /* centraliza título vs. phone */
}
@media (max-width:1024px){
  .hero-inner{ grid-template-columns:1fr; }
  .copy-col{ order:-1; text-align:center; }
}

.brand-badge{
  display:inline-flex; align-items:center; gap:8px;
  background:#eafff0; color:#084a2a; font-weight:800;
  padding:6px 12px; border-radius:999px; box-shadow:0 4px 10px rgba(0,0,0,.06); margin-bottom:10px;
}
.brand-badge .pin{ font-size:18px }

.phone-col{ display:flex; justify-content:center }
.phone-frame{
  position:relative; width:min(420px,90vw); aspect-ratio:9/19.5;
  background:#0f1b4a; border-radius:32px;
  box-shadow:0 18px 40px rgba(0,0,0,.25), inset 0 0 0 10px #1b2a6b;
  padding:14px;
}
.notch{ position:absolute; top:10px; left:50%; transform:translateX(-50%); width:40%; height:18px; background:#0f1b4a; border-bottom-left-radius:14px; border-bottom-right-radius:14px; }
.map-hero{ width:100%; height:100%; border-radius:20px; overflow:hidden; filter:saturate(.9) contrast(1.02) brightness(.98); }

.play-pill{
  position:absolute; top:-14px; left:50%; transform:translateX(-50%);
  background:#2f8dfb; color:#fff; font-weight:800; border-radius:999px; padding:8px 20px;
  box-shadow:0 6px 16px rgba(47,141,251,.35); letter-spacing:.5px; cursor:pointer; user-select:none;
}

.title{ font-size:clamp(32px,4.6vw,52px); line-height:1.1; color:#062b19; margin:6px 0 10px; }
.title span{ color: rgb(9, 126, 38); } /* pedido */
.subtitle{ font-size:18px; color:#0b3b22; opacity:.85; margin-bottom:18px }
.cta-row{ display:flex; gap:12px; flex-wrap:wrap }
.copy-col :deep(.q-btn){ font-weight:800 }
.cta.primary{ background:#3b82f6; color:#fff }
.cta.ghost{ background:transparent; color:#0b3b22 }

.about{ max-width:1100px; margin:0 auto; padding:16px 20px 8px }
.about-card{
  display:grid; grid-template-columns:120px 1fr; gap:16px;
  background:#ffffffee; border-radius:18px; padding:18px; box-shadow:0 8px 20px rgba(0,0,0,.08);
}
@media (max-width:700px){ .about-card{ grid-template-columns:1fr } }
.about-illu{
  width:120px; height:120px; border-radius:16px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(140deg,#e7ffe8,#e7f9ff); font-size:40px;
}
.about-text h2{ margin:0 0 6px }
.about-text p{ margin:0; color:#285e3f }

.how{ max-width:1100px; margin:0 auto; padding:20px; }
.how h2{ margin:8px 0 16px }
.how-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px }
@media (max-width:900px){ .how-grid{ grid-template-columns:1fr } }
.how-card{
  background:#ffffffd9; border-radius:16px; padding:18px; box-shadow:0 8px 20px rgba(0,0,0,.08); backdrop-filter:blur(8px)
}
.how-icon{ font-size:28px; margin-bottom:6px }

.ghost-links{
  max-width:1100px; margin:8px auto 0; padding:0 20px 10px; display:flex; gap:18px; flex-wrap:wrap; color:#0b3b2299
}
.ghost-links a{ cursor:default }

.footer{ text-align:center; color:#0b3b22; padding:24px 12px 40px; opacity:.9 }

.leaflet-popup-content-wrapper{ background:#fff; color:#333; font-size:.95rem; border-radius:10px }
.leaflet-popup-tip{ background:#fff }
b{ color:var(--green-700); font-weight:700 }
small{ color:#777; font-size:.8rem }
</style>
