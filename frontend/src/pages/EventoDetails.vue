<template>
  <q-page class="container">
    <div class="row justify-end q-mb-md">
      <q-btn label="Voltar para o mapa" flat icon="arrow_back" @click="$router.push('/')" />
    </div>

    <div v-if="evento">
      <div class="card q-pa-md q-mb-xl">
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-6">
            <q-img :src="evento.imagem" style="width:100%; height:300px" class="rounded-borders" />
          </div>
          <div class="col-12 col-md-6">
            <h1 class="q-mt-none q-mb-sm" style="color:#166534; font-size:36px; font-weight:900; line-height:1.1">
              {{ evento.titulo }}
            </h1>
            <span class="subtitle-chip q-mb-md">{{ evento.categoria }}</span>
            <div class="text-body1 q-mt-md" style="color:#374151; line-height:1.7">
              {{ evento.descricao }}
            </div>
          </div>
        </div>
      </div>

      <div class="card q-pa-lg q-mb-xl">
        <div class="section-title">
          <q-icon name="emoji_objects" color="amber-8" />
          Curiosidades
        </div>
        <div class="text-body1 q-mb-lg" style="color:#374151; line-height:1.7">
          {{ evento.curiosidades }}
        </div>
        <div class="thumb-strip">
          <img v-for="(img, i) in evento.imagensExtras" :key="i" :src="img" class="thumb" />
        </div>
      </div>

      <div class="card q-pa-lg q-mb-xl">
        <div class="section-title">
          <q-icon name="public" color="green-8" />
          Localização no mapa
        </div>
        <div id="map" class="map q-mb-md"></div>
        <div class="text-body1" style="color:#374151">
          📍 <b>{{ evento.endereco }}</b><br />
          📅 Coletado em <i>{{ evento.data }}</i>
        </div>
      </div>
    </div>

    <div v-else class="text-center q-mt-xl">
      <q-icon name="error_outline" color="red" size="64px" />
      <div class="text-h6 q-mt-md">Evento não encontrado</div>
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
const evento = ref(null)

onMounted(async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/eventos/${route.params.id}/`)
    evento.value = await response.json()

    if (evento.value) {
      await nextTick()

      const map = L.map('map').setView([evento.value.latitude, evento.value.longitude], 15)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map)

      const icon = L.icon({
        iconUrl: evento.value.icone || 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        iconSize: [30, 30],
        iconAnchor: [15, 30]
      })

      L.marker([evento.value.latitude, evento.value.longitude], { icon })
        .addTo(map)
        .bindPopup(`<b>${evento.value.titulo}</b><br>${evento.value.endereco}`)
    }
  } catch (err) {
    console.error('Erro ao carregar evento:', err)
  }
})
</script>
