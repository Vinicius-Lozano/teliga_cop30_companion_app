<template>
  <div style="padding: 1rem;">
    <h1>{{ evento ? evento.nome : "Evento não encontrado" }}</h1>

    <div v-if="evento">
      <img
        v-if="evento.icone"
        :src="evento.icone"
        alt="Ícone do evento"
        style="width: 60px; height: 60px; margin: 1rem 0;"
      />
      <p><strong>Descrição:</strong> {{ evento.descricao }}</p>
      <p><strong>Localização:</strong> {{ evento.latitude }}, {{ evento.longitude }}</p>
      <button @click="voltar" style="margin-top: 1rem;">⬅ Voltar para o mapa</button>
    </div>

    <div v-else>
      <p>Não encontramos informações para este evento.</p>
      <button @click="voltar">⬅ Voltar</button>
    </div>
  </div>
</template>

<script setup>
defineOptions({
  name: 'EventDetailsPage'
})
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const evento = ref(null);

onMounted(async () => {
  const res = await fetch('/eventos.json');
  const dados = await res.json();
  evento.value = dados.find(e => e.id === parseInt(route.params.id));
});

function voltar() {
  router.push('/');
}
</script>
