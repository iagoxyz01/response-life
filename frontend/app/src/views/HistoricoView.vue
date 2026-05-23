<template>
  <div class="container">
    <div class="header">
      <button class="voltar" @click="voltar">← Voltar</button>
      <h2>HISTÓRICO</h2>
    </div>

    <div v-if="agendamentos.length === 0" class="vazio">
      <p>Nenhum agendamento encontrado</p>
    </div>

    <div class="lista" v-else>
      <div
        class="card"
        v-for="ag in agendamentos"
        :key="ag.id"
      >
        <div class="card-info">
          <span class="data">📅 {{ formatarData(ag.data_inicio) }}</span>
          <span class="status" :class="ag.status">{{ ag.status }}</span>
        </div>

        <button
          v-if="ag.status === 'concluido'"
          class="btn-avaliar"
          @click="avaliar(ag.id)"
        >
          Avaliar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const agendamentos = ref<any[]>([])

onMounted(async () => {
  try {
    const response = await api.get('/agendamentos/meus')
    agendamentos.value = response.data
  } catch (e) {
    console.error(e)
  }
})

function formatarData(data: string) {
  return new Date(data).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function avaliar(id: number) {
  router.push(`/avaliacao/${id}`)
}

function voltar() {
  router.push('/home-cliente')
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f0f4f8;
  padding: 1rem;
}

.header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.header h2 {
  color: #2c7a7b;
  margin: 0;
}

.voltar {
  background: none;
  border: none;
  color: #2c7a7b;
  font-size: 1rem;
  cursor: pointer;
  padding: 0;
}

.vazio {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  color: #718096;
}

.lista {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  background: white;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.card-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.data {
  color: #2d3748;
  font-weight: 500;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status.pendente {
  background: #fef3c7;
  color: #92400e;
}

.status.concluido {
  background: #d1fae5;
  color: #065f46;
}

.status.cancelado {
  background: #fee2e2;
  color: #991b1b;
}

.btn-avaliar {
  width: 100%;
  padding: 0.5rem;
  background: #2c7a7b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
}
</style>