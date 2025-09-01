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

        <q-form @submit.prevent="saveEvento" enctype="multipart/form-data">
          <q-card-section class="q-gutter-md">
            <q-input v-model="form.titulo" label="Título" filled :rules="[val => !!val || 'O título é obrigatório']" />
            <q-input v-model="form.categoria" label="Categoria" filled />
            <q-input v-model="form.descricao" label="Descrição" type="textarea" filled />
            <q-input v-model="form.curiosidades" label="Curiosidades" type="textarea" filled />
            <q-input v-model="form.endereco" label="Endereço" filled />
            <div class="row q-col-gutter-md">
              <div class="col"><q-input v-model.number="form.latitude" label="Latitude" type="number" step="any" filled /></div>
              <div class="col"><q-input v-model.number="form.longitude" label="Longitude" type="number" step="any" filled /></div>
            </div>
            <div class="row q-col-gutter-md">
              <div class="col"><q-input v-model="form.data" label="Data" type="date" stack-label filled /></div>
              <div class="col"><q-input v-model="form.horario" label="Horário" type="time" stack-label filled /></div>
            </div>
            <q-input v-model="form.icone" label="URL do Ícone do Mapa" filled />
            <q-file v-model="form.imagem" label="Imagem Principal do Evento" filled accept="image/*">
              <template v-slot:prepend><q-icon name="cloud_upload" /></template>
            </q-file>
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

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'

const $q = useQuasar()
const eventos = ref([])
const loading = ref(false)
const showForm = ref(false)
const isSaving = ref(false)

// Estado inicial do formulário correspondendo ao models.py
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

// Colunas da tabela atualizadas para o seu modelo
const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'titulo', label: 'Título', field: 'titulo', align: 'left', sortable: true },
  { name: 'imagem', label: 'Imagem', field: 'imagem', align: 'center' },
  { name: 'categoria', label: 'Categoria', field: 'categoria', align: 'left', sortable: true },
  { name: 'data', label: 'Data', field: 'data', align: 'left', sortable: true },
  { name: 'horario', label: 'Horário', field: 'horario', align: 'left', sortable: true },
  { name: 'actions', label: 'Ações', align: 'center' }
]

const backendUrl = 'http://127.0.0.1:8000'
function getImageUrl(imagePath) {
  if (!imagePath) return ''
  return imagePath.startsWith('http') ? imagePath : `${backendUrl}${imagePath}`
}

async function fetchEventos() {
  loading.value = true
  try {
    const response = await api.get('/api/events/fixed/')
    eventos.value = response.data
  } catch (error) {
    console.error('Erro ao carregar eventos:', error)
    $q.notify({ type: 'negative', message: 'Erro ao carregar eventos' })
  } finally {
    loading.value = false
  }
}

function openForm(evento = null) {
  if (evento) {
    form.value = { ...evento, imagem: null }
  } else {
    form.value = { ...formInitialState }
  }
  showForm.value = true
}

async function saveEvento() {
  isSaving.value = true
  const formData = new FormData()

  // Mapeia todos os campos do formulário para o FormData
  Object.keys(form.value).forEach(key => {
    const value = form.value[key]
    if (key === 'imagem' && value instanceof File) {
      formData.append(key, value)
    } else if (key !== 'imagem' && value !== null) { // CORREÇÃO: Permite o envio de strings vazias para validação no backend
      // JSON.stringify para o campo de imagens extras
      if (key === 'imagens_extras') {
        formData.append(key, JSON.stringify(value))
      } else {
        formData.append(key, value)
      }
    }
  })

  try {
    if (form.value.id) {
      await api.patch(`/api/events/fixed/${form.value.id}/`, formData)
      $q.notify({ type: 'positive', message: 'Evento atualizado!' })
    } else {
      await api.post('/api/events/fixed/', formData)
      $q.notify({ type: 'positive', message: 'Evento criado!' })
    }
    showForm.value = false
    fetchEventos()
  } catch (error) {
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
      await api.delete(`/api/events/fixed/${id}/`)
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

