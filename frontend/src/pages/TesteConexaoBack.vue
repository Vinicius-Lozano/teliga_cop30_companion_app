<template>
  <q-page class="flex flex-center column text-center q-pa-md">
    <div v-if="loading">
      <q-spinner-dots color="primary" size="3em" />
      <div class="q-mt-md text-grey-8">Testando conexão com o backend...</div>
    </div>

    <div v-if="error">
      <q-icon name="sym_o_error" color="negative" size="4em" />
      <h5 class="text-negative q-mt-sm q-mb-xs">Falha na Conexão</h5>
      <p>Não foi possível conectar ao backend. Verifique se o servidor Django está rodando.</p>
      <pre class="error-details">{{ error }}</pre>
    </div>

    <div v-if="message">
      <q-icon name="sym_o_cloud_done" color="positive" size="4em" />
      <h5 class="text-positive q-mt-sm q-mb-xs">Sucesso!</h5>
      <p class="text-h6 text-grey-8">"{{ message }}"</p>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineOptions({
  name: 'TestConnectionPage'
})

const loading = ref(true)
const message = ref('')
const error = ref(null)

onMounted(async () => {
  try {
    const apiUrl = `${import.meta.env.VITE_API_URL}/teste_rota_back/`
    const response = await fetch(apiUrl)
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`)
    }
    const data = await response.json()
    message.value = data.message
  } catch (e) {
    error.value = e.message
    console.error('Erro ao testar conexão:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.error-details {
  background-color: #ffebee;
  border: 1px solid #e57373;
  padding: 1rem;
  border-radius: 4px;
  color: #c62828;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-width: 600px;
  margin: 0 auto;
}
</style>