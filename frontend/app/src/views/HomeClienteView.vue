<template>
  <div class="container">
    <div class="header">
      <h2>HOME</h2>
      <button class="logout" @click="sair">Sair</button>
    </div>

    <div class="boas-vindas">
      <h3>Olá, {{ nomeUsuario }} 👤</h3>
      <p>Agendamentos: {{ totalAgendamentos }}</p>
    </div>

    <div class="menu">
      <button class="btn-menu" @click="irPara('/agendamento')">
        Novo Agendamento →
      </button>
      <button class="btn-menu" @click="irPara('/historico')">
        Histórico
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

const nomeUsuario = ref('')
const totalAgendamentos = ref(0)

onMounted(async () => {
  try {
    const response = await api.get('/agendamentos/meus')
    totalAgendamentos.value = response.data.length
  } catch (e) {
    console.error(e)
  }

  const tipo = authStore.tipo
  nomeUsuario.value = tipo === 'cliente' ? 'Cliente' : 'Usuário'
})

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
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.boas-vindas h3 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 1.25rem;
}

.boas-vindas p {
  margin: 0;
  color: #718096;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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