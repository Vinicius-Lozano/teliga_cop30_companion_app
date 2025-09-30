<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h4">Gerenciar Eventos</div>
      <q-btn color="primary" label="Novo Evento" @click="openForm()" icon="add" />
    </div>

    <q-table
      :rows="eventos"
      :columns="columns"
      row-key="id"
      flat
      bordered
      :loading="loading"
    >
      <template v-slot:body-cell-imagem="props">
        <q-td :props="props">
          <q-img
            v-if="props.row.imagem"
            :src="getImageUrl(props.row.imagem)"
            spinner-color="white"
            style="height: 60px; max-width: 100px; border-radius: 4px;"
            fit="cover"
          />
          <span v-else class="text-grey-7">N/A</span>
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td align-center class="q-gutter-sm">
          <q-btn dense flat icon="edit" color="primary" @click="openForm(props.row)" />
          <q-btn dense flat icon="delete" color="negative" @click="deleteEvento(props.row.id)" />
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="showForm">
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">{{ form.id ? 'Editar Evento' : 'Novo Evento' }}</div>
        </q-card-section>

        <q-form @submit.prevent="saveEvento">
          <q-card-section class="q-gutter-md">
            <q-input v-model="form.titulo" label="Título" filled :rules="[val => !!val || 'O título é obrigatório']" />
            <q-input v-model="form.categoria" label="Categoria" filled />
            <q-input v-model="form.descricao" label="Descrição" type="textarea" filled />
            <q-input v-model="form.curiosidades" label="Curiosidades" type="textarea" filled />
            <q-input v-model="form.endereco" label="Endereço" filled />
            
            <div class="map-container">
              <l-map v-model:zoom="mapZoom" :center="mapCenter" @click="handleMapClick" style="height: 100%;">
                <l-tile-layer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  layer-type="base" name="OpenStreetMap"
                  attribution="&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
                />
                <l-marker v-if="markerLatLng" :lat-lng="markerLatLng" />
              </l-map>
            </div>
            
            <div class="row q-col-gutter-md">
              <div class="col"><q-input v-model.number="form.latitude" label="Latitude" type="number" step="any" filled /></div>
              <div class="col"><q-input v-model.number="form.longitude" label="Longitude" type="number" step="any" filled /></div>
            </div>
            
            <div class="row q-col-gutter-md">
              <div class="col"><q-input v-model="form.data" label="Data" type="date" stack-label filled /></div>
              <div class="col"><q-input v-model="form.horario" label="Horário" type="time" stack-label filled /></div>
            </div>

            <div class="row items-center q-gutter-md">
              <div class="col">
                <q-file
                  v-model="imageFile"
                  label="Imagem Principal do Evento"
                  filled
                  accept="image/*"
                  :loading="isUploadingImage"
                  @update:model-value="handleImageUpload"
                >
                  <template v-slot:prepend><q-icon name="cloud_upload" /></template>
                </q-file>
              </div>
              <div v-if="uploadedImageUrl">
                <q-img
                  :src="uploadedImageUrl"
                  spinner-color="white"
                  style="height: 60px; width: 100px; border-radius: 4px;"
                />
              </div>
            </div>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn color="primary" label="Salvar" type="submit" :loading="isSaving" />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style>
.map-container {
  height: 300px;
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
}
</style>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

const $q = useQuasar()
const eventos = ref([])
const loading = ref(false)
const showForm = ref(false)
const isSaving = ref(false)

// Estado do Mapa
const mapZoom = ref(13);
const mapCenter = ref([-1.4558, -48.5039]);
const markerLatLng = ref(null);

// Estados para o upload de imagem
const imageFile = ref(null)
const uploadedImageUrl = ref(null)
const isUploadingImage = ref(false)

const formInitialState = {
  id: null,
  titulo: '',
  categoria: '',
  imagem: null,
  descricao: '',
  curiosidades: '',
  endereco: '',
  data: null,
  horario: null,
  latitude: null,
  longitude: null,
  icone: '',
  imagens_extras: [],
}
const form = ref({ ...formInitialState })

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'titulo', label: 'Título', field: 'titulo', align: 'left', sortable: true },
  { name: 'imagem', label: 'Imagem', field: 'imagem', align: 'center' },
  { name: 'categoria', label: 'Categoria', field: 'categoria', align: 'left', sortable: true },
  { name: 'data', label: 'Data', field: 'data', align: 'left', sortable: true },
  { name: 'horario', label: 'Horário', field: 'horario', align: 'left', sortable: true },
  { name: 'actions', label: 'Ações', align: 'center' }
]

function getImageUrl(imagePath) {
  return imagePath || ''
}

async function handleImageUpload(file) {
  if (!file) {
    uploadedImageUrl.value = null;
    return
  }
  isUploadingImage.value = true

  const formData = new FormData();
  formData.append('image', file);

  try {
    // Faz a chamada para o endpoint no backend Django
    const response = await api.post('/api/events/upload-image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // A resposta do Django conterá a URL final do Supabase
    uploadedImageUrl.value = response.data.imageUrl;

    $q.notify({ type: 'positive', message: 'Imagem enviada com sucesso!' })

  } catch (error) {
    console.error('Erro no upload da imagem:', error.response?.data || error)
    $q.notify({ type: 'negative', message: 'Erro ao enviar a imagem.' })
    imageFile.value = null
    uploadedImageUrl.value = null
  } finally {
    isUploadingImage.value = false
  }
}

async function fetchEventos() {
  loading.value = true
  try {
    const response = await api.get('/api/events/')
    eventos.value = response.data
  } catch (error) {
    console.error('Erro ao carregar eventos:', error)
    $q.notify({ type: 'negative', message: 'Erro ao carregar eventos' })
  } finally {
    loading.value = false
  }
}

function handleMapClick(event) {
  const { lat, lng } = event.latlng;
  form.value.latitude = parseFloat(lat.toFixed(6));
  form.value.longitude = parseFloat(lng.toFixed(6));
}

watch(() => [form.value.latitude, form.value.longitude], ([newLat, newLng]) => {
  if (newLat !== null && newLng !== null && typeof newLat === 'number' && typeof newLng === 'number') {
    const newPosition = [newLat, newLng];
    markerLatLng.value = newPosition;
    mapCenter.value = newPosition;
  } else {
    markerLatLng.value = null;
  }
});

function openForm(evento = null) {
  imageFile.value = null
  uploadedImageUrl.value = null
  markerLatLng.value = null
  mapCenter.value = [-1.4558, -48.5039]

  if (evento) {
    form.value = { ...evento }
    if (evento.imagem) {
      uploadedImageUrl.value = evento.imagem
    }
    if (evento.latitude && evento.longitude) {
      const position = [evento.latitude, evento.longitude];
      mapCenter.value = position;
      markerLatLng.value = position;
    }
  } else {
    form.value = { ...formInitialState }
  }
  showForm.value = true
}

async function saveEvento() {
  isSaving.value = true
  const payload = { ...form.value }
  payload.imagem = uploadedImageUrl.value

  try {
    if (payload.id) {
      await api.patch(`/api/events/${payload.id}/`, payload)
      $q.notify({ type: 'positive', message: 'Evento atualizado!' })
    } else {
      await api.post('/api/events/', payload)
      $q.notify({ type: 'positive', message: 'Evento criado!' })
    }
    showForm.value = false
    fetchEventos()
  } catch (error)
 {
    console.error('Erro ao salvar evento:', error.response?.data || error)
    $q.notify({ type: 'negative', message: 'Erro ao salvar evento. Verifique o console.' })
  } finally {
    isSaving.value = false
  }
}

function deleteEvento(id) {
  $q.dialog({
    title: 'Confirmar Exclusão',
    message: 'Tem certeza que deseja excluir este evento?',
    ok: { label: 'Excluir', color: 'negative' },
    cancel: { label: 'Cancelar', flat: true },
  }).onOk(async () => {
    try {
      await api.delete(`/api/events/${id}/`)
      $q.notify({ type: 'positive', message: 'Evento removido!' })
      fetchEventos()
    } catch (error) {
      console.error('Erro ao excluir evento:', error)
      $q.notify({ type: 'negative', message: 'Erro ao excluir evento' })
    }
  })
}

onMounted(fetchEventos)
</script>