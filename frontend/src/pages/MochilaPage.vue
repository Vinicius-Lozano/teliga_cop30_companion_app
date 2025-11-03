<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card class="main-card q-pa-lg q-ma-md">
      <div class="row items-center q-mb-lg">
        <q-btn
          flat
          round
          dense
          icon="arrow_back"
          color="primary"
          @click="$router.back()"
        />
        <div class="text-h5 text-primary text-weight-bold q-ml-md">
          🎒 Minha Mochila
        </div>
      </div>

      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="fauna" label="Fauna" icon="pets" />
        <q-tab name="flora" label="Flora" icon="grass" />
        <q-tab name="itens" label="Itens" icon="inventory_2" />
        <q-tab name="pocoes" label="Poções" icon="science" />
        <q-tab name="eventos" label="Eventos" icon="event" />
      </q-tabs>

      <q-separator class="q-mb-lg" />

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="fauna" class="q-pa-none">
          <div v-if="fauna.length === 0" class="text-grey-7 text-italic q-mt-md text-center">
            Você ainda não capturou nenhuma fauna.
          </div>
          <div class="item-grid">
            <q-card
              v-for="captura in fauna"
              :key="captura.id"
              flat
              bordered
              class="item-card"
              @click="abrirModalDetalhe(captura.item, 'fauna', captura.foi_captura_forcada, captura.id, captura.captured_at)"
            >
              <q-img :src="captura.item.imagem || 'https://i.imgur.com/qL4lF3c.png'" :ratio="1">
                <div class="absolute-bottom text-subtitle2 text-center">
                  {{ captura.item.nome }}
                </div>
              </q-img>
            </q-card>
          </div>
        </q-tab-panel>

        <q-tab-panel name="flora" class="q-pa-none">
           <div v-if="flora.length === 0" class="text-grey-7 text-italic q-mt-md text-center">
            Você ainda não capturou nenhuma flora.
          </div>
          <div class="item-grid">
            <q-card
              v-for="captura in flora"
              :key="captura.id"
              flat
              bordered
              class="item-card"
              @click="abrirModalDetalhe(captura.item, 'flora', captura.foi_captura_forcada, captura.id, captura.captured_at)"
            >
              <q-img :src="captura.item.imagem || 'https://i.imgur.com/qL4lF3c.png'" :ratio="1">
                <div class="absolute-bottom text-subtitle2 text-center">
                  {{ captura.item.nome }}
                </div>
              </q-img>
            </q-card>
          </div>
        </q-tab-panel>

        <q-tab-panel name="itens" class="q-pa-none">
          <div v-if="itens.length === 0" class="text-grey-7 text-italic q-mt-md text-center">
            Você ainda não capturou nenhum item.
          </div>
          <div class="item-grid">
            <q-card
              v-for="captura in itens"
              :key="captura.id"
              flat
              bordered
              class="item-card"
              @click="abrirModalDetalhe(captura.item, 'item', false, captura.id, captura.captured_at)"
            >
              <q-img :src="captura.item.imagem || 'https://i.imgur.com/qL4lF3c.png'" :ratio="1">
                <div class="absolute-bottom text-subtitle2 text-center">
                  {{ captura.item.nome }}
                </div>
              </q-img>
            </q-card>
          </div>
        </q-tab-panel>

        <q-tab-panel name="pocoes" class="q-pa-none">
           <div v-if="pocoes.length === 0" class="text-grey-7 text-italic q-mt-md text-center">
            Você ainda não capturou nenhuma poção.
          </div>
          <div class="item-grid">
            <q-card
              v-for="captura in pocoes"
              :key="captura.id"
              flat
              bordered
              class="item-card"
              @click="abrirModalDetalhe(captura.item, 'pocao', false, captura.id, captura.captured_at)"
            >
              <q-img :src="captura.item.imagem || 'https://i.imgur.com/qL4lF3c.png'" :ratio="1">
                <div class="absolute-bottom text-subtitle2 text-center">
                  {{ captura.item.nome }}
                </div>
              </q-img>
            </q-card>
          </div>
        </q-tab-panel>

        <q-tab-panel name="eventos" class="q-pa-none">
           <div v-if="eventos.length === 0" class="text-grey-7 text-italic q-mt-md text-center">
            Você ainda não participou de nenhum evento.
          </div>
          <div class="item-grid">
             <q-card
              v-for="captura in eventos"
              :key="captura.id"
              flat
              bordered
              class="item-card"
              @click="abrirModalDetalhe(captura.evento, 'evento', false, captura.id, captura.captured_at)"
            >
              <q-img :src="captura.evento.imagem || 'https://i.imgur.com/qL4lF3c.png'" :ratio="1">
                <div class="absolute-bottom text-subtitle2 text-center">
                  {{ captura.evento.titulo }}
                </div>
              </q-img>
            </q-card>
          </div>
        </q-tab-panel>

      </q-tab-panels>
    </q-card>

    <q-dialog v-model="modalDetalheAberto">
      <q-card style="width: 400px; max-width: 90vw;">
        <q-img :src="itemSelecionado?.imagem || 'https://i.imgur.com/qL4lF3c.png'" :ratio="16/9" />

        <q-card-section>
          <div class="text-h5 text-weight-bold">{{ itemSelecionado?.nome || itemSelecionado?.titulo }}</div>
          <div class="text-caption text-grey text-capitalize">{{ tipoItemSelecionado }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <p>{{ itemSelecionado?.descricao || itemSelecionado?.categoria }}</p>

          <div v-if="tipoItemSelecionado === 'pocao' && itemSelecionado?.bonus_captura">
            <q-icon name="arrow_upward" color="positive" />
            Bônus de Captura: +{{ itemSelecionado.bonus_captura }}%
          </div>

          <div v-if="tipoItemSelecionado === 'fauna' && foiForcada" class="q-mt-md text-negative">
            <q-icon name="warning" />
            <span>Capturado à força</span>
          </div>
           <div v-if="tipoItemSelecionado === 'fauna' && !foiForcada" class="q-mt-md text-positive">
            <q-icon name="check_circle" />
            <span>Capturado em harmonia</span>
          </div>

          <div v-if="tipoItemSelecionado === 'fauna' && dataCapturaSelecionada" class="q-mt-md text-grey-8">
            <q-icon name="calendar_month" class="q-mr-xs" />
            Capturado em: {{ formatarData(dataCapturaSelecionada) }}
          </div>
          </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Fechar" color="primary" v-close-popup />
          <q-btn 
            v-if="tipoItemSelecionado === 'evento'"
            flat 
            label="Remover" 
            color="negative" 
            @click="confirmarRemocao" 
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="dialogRemocaoAberto" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-icon name="warning" color="warning" size="md" class="q-mr-sm" />
          <div class="text-h6">Remover evento</div>
        </q-card-section>
        <q-card-section>
          Tem certeza que deseja remover o evento
          <b>{{ itemSelecionado?.titulo }}</b> da mochila?
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="grey" v-close-popup />
          <q-btn flat label="Remover" color="negative" @click="removerEventoConfirmado" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useQuasar } from "quasar";
import { api } from "boot/axios";

const $q = useQuasar();

// --- STATE ---
const tab = ref("fauna");

// Listas de dados
const itens = ref([]);
const pocoes = ref([]);
const eventos = ref([]);
const fauna = ref([]);
const flora = ref([]);

// State dos Modais
const modalDetalheAberto = ref(false);
const dialogRemocaoAberto = ref(false);
const itemSelecionado = ref(null);
const tipoItemSelecionado = ref("");
const foiForcada = ref(false);
const idCapturaSelecionada = ref(null);
const dataCapturaSelecionada = ref(null); 

// --- LIFECYCLE ---
onMounted(async () => {
  try {
    const [resFauna, resFlora, resItens, resPocoes, resEventos] = await Promise.all([
      api.get("/api/capturas/fauna/"),
      api.get("/api/capturas/flora/"),
      api.get("/api/capturas/itens/"),
      api.get("/api/capturas/pocoes/"),
      api.get("/api/capturas/eventos/")
    ]);

    fauna.value = resFauna.data;
    flora.value = resFlora.data;
    itens.value = resItens.data;
    pocoes.value = resPocoes.data;
    eventos.value = resEventos.data;

  } catch (err) {
    console.error(err);
    $q.notify({ type: "negative", message: "Erro ao carregar mochila" });
  }
});

// --- MÉTODOS ---

function abrirModalDetalhe(item, tipo, capturaForcada, idCaptura, dataCaptura) {
  itemSelecionado.value = item;
  tipoItemSelecionado.value = tipo;
  foiForcada.value = capturaForcada;
  idCapturaSelecionada.value = idCaptura;
  dataCapturaSelecionada.value = dataCaptura; 
  modalDetalheAberto.value = true;
}

function confirmarRemocao() {
  modalDetalheAberto.value = false; 
  dialogRemocaoAberto.value = true; 
}

async function removerEventoConfirmado() {
  if (!idCapturaSelecionada.value) return;
  try {
    // Deleta usando o ID da captura (MochilaEvento)
    await api.delete(`/api/capturas/eventos/${idCapturaSelecionada.value}/`);
    
    // Remove da lista local
    eventos.value = eventos.value.filter((e) => e.id !== idCapturaSelecionada.value);
    
    $q.notify({ type: "positive", message: "Evento removido com sucesso!" });
  
  } catch (error) {
    console.error("Erro ao remover evento:", error);
    $q.notify({ type: "negative", message: "Não foi possível remover o evento." });
  
  } finally {
    dialogRemocaoAberto.value = false;
    itemSelecionado.value = null;
    idCapturaSelecionada.value = null;
    dataCapturaSelecionada.value = null; 
  }
}

// --- FUNÇÃO HELPER ADICIONADA ---
function formatarData(dataISO) {
  if (!dataISO) return '';
  return new Date(dataISO).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
}
</script>

<style scoped>
.main-card {
  max-width: 1100px;
  width: 100%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  min-height: 70vh;
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
}

.item-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 8px;
  overflow: hidden;
}
.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}

.text-h5 {
  font-size: 1.7rem;
}
</style>