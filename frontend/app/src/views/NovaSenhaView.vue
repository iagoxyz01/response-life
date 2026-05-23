 
<template>
  <div class="container">
    <div class="card">
      <h1>Response Life</h1>
      <p class="subtitle">Criar nova senha</p>

      <div v-if="erro" class="erro">{{ erro }}</div>
      <div v-if="sucesso" class="sucesso">
        ✅ Senha alterada! Redirecionando...
      </div>

      <div class="campo">
        <label>Nova senha</label>
        <input v-model="novaSenha" type="password" placeholder="mínimo 6 caracteres" />
      </div>

      <div class="campo">
        <label>Confirmar senha</label>
        <input v-model="confirmarSenha" type="password" placeholder="repita a senha" />
      </div>

      <button @click="salvar" :disabled="carregando">
        {{ carregando ? 'Salvando...' : 'Salvar nova senha' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api'

const router = useRouter()
const route = useRoute()

const novaSenha = ref('')
const confirmarSenha = ref('')
const erro = ref('')
const sucesso = ref(false)
const carregando = ref(false)
const token = ref('')

onMounted(() => {
  token.value = route.query.token as string
  if (!token.value) {
    erro.value = 'Token inválido'
  }
})

async function salvar() {
  erro.value = ''

  if (novaSenha.value.length < 6) {
    erro.value = 'Senha deve ter no mínimo 6 caracteres'
    return
  }

  if (novaSenha.value !== confirmarSenha.value) {
    erro.value = 'As senhas não coincidem'
    return
  }

  carregando.value = true
  try {
    await api.post('/usuarios/nova-senha', {
      token: token.value,
      nova_senha: novaSenha.value,
    })
    sucesso.value = true
    setTimeout(() => router.push('/'), 2000)
  } catch (e: any) {
    erro.value = e.response?.data?.detail || 'Erro ao alterar senha'
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f4f8;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  color: #2c7a7b;
  text-align: center;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #718096;
  margin-bottom: 1.5rem;
}

.campo {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.25rem;
  color: #4a5568;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #2c7a7b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}

button:disabled { opacity: 0.6; }

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