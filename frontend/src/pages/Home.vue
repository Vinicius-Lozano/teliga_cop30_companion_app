<template>
  <div>
    <!-- Banner -->
    <header class="banner">
      <h1>Te Liga!</h1>
      <p>Bem-vindo(a) ao mapa de eventos!</p>
    </header>

    <!-- Mapa -->
    <l-map
      style="height: 80vh; width: 100%;"
      :zoom="13"
      :center="[-1.4558, -48.4902]"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      <l-marker
        v-for="evento in eventos"
        :key="evento.id"
        :lat-lng="[evento.latitude, evento.longitude]"
        @click="irParaDetalhes(evento.id)"
      >
        <l-icon
          :icon-url="evento.icone"
          :icon-size="[40, 40]"
        />
      </l-marker>
    </l-map>
  </div>
</template>

<script setup>
defineOptions({
  name: 'HomePage'
})
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { LMap, LTileLayer, LMarker, LIcon } from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';

const eventos = ref([]);
const router = useRouter();

function irParaDetalhes(id) {
  router.push(`/details/${id}`);
}

onMounted(async () => {
  const res = await fetch('/eventos.json');
  eventos.value = await res.json();
});
</script>


<style scoped>
.banner {
  background-color: #2e7d32;
  color: white;
  text-align: center;
  padding: 2rem 1rem;
}

.banner h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.banner p {
  font-size: 1.2rem;
  margin: 0;
}
</style>
