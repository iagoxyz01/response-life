<template>
  <div class="container">
    <div class="header">
      <h2>HOME</h2>
      <button class="logout" @click="sair">Sair</button>
    </div>

    <div class="boas-vindas">
      <h3>Olá, Cuidador 👤</h3>
      <p>Próximos atendimentos</p>
    </div>

    <div class="agendamentos" v-if="agendamentos.length > 0">
      <div
        class="agendamento-card"
        v-for="ag in agendamentos"
        :key="ag.id"
      >
        <span>📅 {{ formatarData(ag.data_inicio) }}</span>
        <span class="status" :class="ag.status">{{ ag.status }}</span>
      </div>
    </div>

    <div class="vazio" v-else>
      <p>Nenhum atendimento pendente</p>
    </div>

    <div class="menu">
      <button class="btn-menu" @click="irPara('/cadastro-servico')">
        Cadastrar Serviço →
      </button>
      <button class="btn-menu" @click="irPara('/avaliacoes')">
        Avaliações
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()
const agendamentos = ref<any[]>([])

onMounted(async () => {
  try {
    const response = await api.get('/agendamentos/meus')
    agendamentos.value = response.data.filter(
      (ag: any) => ag.status === 'pendente'
    )
  } catch (e) {
    console.error(e)
  }
})

function formatarData(data: string) {
  return new Date(data).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function irPara(rota: string) {
  router.push(rota)
}

function sair() {
  authStore.logout()
  router.push('/')
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
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header h2 {
  color: #2c7a7b;
  margin: 0;
}

.logout {
  background: none;
  border: 1px solid #2c7a7b;
  color: #2c7a7b;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
}

.boas-vindas {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.boas-vindas h3 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
}

.boas-vindas p {
  margin: 0;
  color: #718096;
}

.agendamentos {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.agendamento-card {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
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

.vazio {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  color: #718096;
  margin-bottom: 1rem;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-menu {
  background: white;
  border: none;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
  text-align: left;
  font-size: 1rem;
  color: #2d3748;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  font-weight: 500;
}

.btn-menu:hover {
  background: #2c7a7b;
  color: white;
}
</style>