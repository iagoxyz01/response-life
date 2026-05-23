<template>
  <div class="container">
    <div class="header">
      <button class="voltar" @click="voltar">← Voltar</button>
      <h2>AGENDAMENTO</h2>
    </div>

    <div v-if="sucesso" class="sucesso">
      ✅ Agendamento criado com sucesso!
    </div>

    <div v-if="erro" class="erro">{{ erro }}</div>

    <div class="form">
      <div class="campo">
        <label>Data início</label>
        <input v-model="dataInicio" type="datetime-local" required />
      </div>

      <div class="campo">
        <label>Data fim</label>
        <input v-model="dataFim" type="datetime-local" required />
      </div>

      <div class="campo">
        <label>Serviço</label>
        <select v-model="servicoId">
          <option value="">Selecione um serviço</option>
          <option
            v-for="servico in servicos"
            :key="servico.id"
            :value="servico.id"
          >
            {{ servico.nome }}
          </option>
        </select>
      </div>

      <button class="btn-confirmar" @click="confirmar" :disabled="carregando">
        {{ carregando ? 'Agendando...' : 'Confirmar' }}
      </button>

      <button class="btn-cancelar" @click="voltar">
        Cancelar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const dataInicio = ref('')
const dataFim = ref('')
const servicoId = ref('')
const servicos = ref<any[]>([])
const carregando = ref(false)
const erro = ref('')
const sucesso = ref(false)

onMounted(async () => {
  try {
    const response = await api.get('/servicos/')
    servicos.value = response.data
  } catch (e) {
    console.error(e)
  }
})

async function confirmar() {
  erro.value = ''
  sucesso.value = false

  if (!dataInicio.value || !dataFim.value || !servicoId.value) {
    erro.value = 'Preencha todos os campos'
    return
  }

  carregando.value = true
  try {
    await api.post('/agendamentos/', {
      data_inicio: dataInicio.value,
      data_fim: dataFim.value,
      servico_id: Number(servicoId.value),
    })
    sucesso.value = true
    setTimeout(() => router.push('/home-cliente'), 2000)
  } catch (e: any) {
    erro.value = e.response?.data?.detail || 'Erro ao criar agendamento'
  } finally {
    carregando.value = false
  }
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

.form {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.campo {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.25rem;
  color: #4a5568;
  font-weight: 500;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

.btn-confirmar {
  width: 100%;
  padding: 0.75rem;
  background: #2c7a7b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.btn-confirmar:disabled {
  opacity: 0.6;
}

.btn-cancelar {
  width: 100%;
  padding: 0.75rem;
  background: white;
  color: #718096;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.sucesso {
  background: #d1fae5;
  color: #065f46;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}

.erro {
  background: #fff5f5;
  color: #c53030;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}
</style>