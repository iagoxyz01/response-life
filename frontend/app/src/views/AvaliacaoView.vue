 <template>
  <div class="container">
    <div class="header">
      <button class="voltar" @click="voltar">← Voltar</button>
      <h2>AVALIAÇÃO</h2>
    </div>

    <div v-if="erro" class="erro">{{ erro }}</div>
    <div v-if="sucesso" class="sucesso">✅ Avaliação enviada!</div>

    <div class="form">
      <div class="campo">
        <label>Nota</label>
        <div class="estrelas">
          <span
            v-for="n in 5"
            :key="n"
            class="estrela"
            :class="{ ativa: n <= nota }"
            @click="nota = n"
          >★</span>
        </div>
      </div>

      <div class="campo">
        <label>Comentário</label>
        <textarea
          v-model="comentario"
          placeholder="Como foi o atendimento?"
          rows="4"
        ></textarea>
      </div>

      <button class="btn-enviar" @click="enviar" :disabled="carregando">
        {{ carregando ? 'Enviando...' : 'Enviar Avaliação' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api'

const router = useRouter()
const route = useRoute()

const nota = ref(0)
const comentario = ref('')
const erro = ref('')
const sucesso = ref(false)
const carregando = ref(false)

const agendamentoId = Number(route.params.id)

async function enviar() {
  erro.value = ''

  if (nota.value === 0) {
    erro.value = 'Selecione uma nota'
    return
  }

  carregando.value = true
  try {
    await api.post('/avaliacoes/', {
      agendamento_id: agendamentoId,
      nota: nota.value,
      comentario: comentario.value,
    })
    sucesso.value = true
    setTimeout(() => router.push('/historico'), 2000)
  } catch (e: any) {
    erro.value = e.response?.data?.detail || 'Erro ao enviar avaliação'
  } finally {
    carregando.value = false
  }
}

function voltar() {
  router.push('/historico')
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
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 500;
}

.estrelas {
  display: flex;
  gap: 0.5rem;
}

.estrela {
  font-size: 2.5rem;
  cursor: pointer;
  color: #e2e8f0;
  transition: color 0.2s;
}

.estrela.ativa {
  color: #f6ad55;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  font-family: inherit;
}

.btn-enviar {
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

.btn-enviar:disabled {
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
