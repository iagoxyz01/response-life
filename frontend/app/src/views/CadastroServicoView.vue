 <template>
  <div class="container">
    <div class="header">
      <button class="voltar" @click="voltar">← Voltar</button>
      <h2>NOVO SERVIÇO</h2>
    </div>

    <div v-if="erro" class="erro">{{ erro }}</div>
    <div v-if="sucesso" class="sucesso">✅ Serviço cadastrado!</div>

    <div class="form">
      <div class="campo">
        <label>Nome do serviço</label>
        <input v-model="nome" type="text" placeholder="Ex: Acompanhamento diário" />
      </div>

      <div class="campo">
        <label>Descrição</label>
        <textarea v-model="descricao" placeholder="Descreva o serviço oferecido" rows="4"></textarea>
      </div>

      <button class="btn-salvar" @click="salvar" :disabled="carregando">
        {{ carregando ? 'Salvando...' : '[ Salvar' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const nome = ref('')
const descricao = ref('')
const erro = ref('')
const sucesso = ref(false)
const carregando = ref(false)

async function salvar() {
  erro.value = ''

  if (!nome.value || !descricao.value) {
    erro.value = 'Preencha todos os campos'
    return
  }

  carregando.value = true
  try {
    await api.post('/servicos/', {
      nome: nome.value,
      descricao: descricao.value,
    })
    sucesso.value = true
    setTimeout(() => router.push('/home-cuidador'), 2000)
  } catch (e: any) {
    erro.value = e.response?.data?.detail || 'Erro ao cadastrar serviço'
  } finally {
    carregando.value = false
  }
}

function voltar() {
  router.push('/home-cuidador')
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

input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  font-family: inherit;
}

.btn-salvar {
  width: 100%;
  padding: 0.75rem;
  background: #2c7a7b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 600;
}

.btn-salvar:disabled {
  opacity: 0.6;
}

.erro {
  background: #fff5f5;
  color: #c53030;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}

.sucesso {
  background: #d1fae5;
  color: #065f46;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}
</style>
