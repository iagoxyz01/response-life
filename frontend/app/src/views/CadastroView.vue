<template>
  <div class="container">
    <div class="card">
      <h1>Response Life</h1>
      <p class="subtitle">Criar nova conta</p>

      <div v-if="erro" class="erro">{{ erro }}</div>
      <div v-if="sucesso" class="sucesso">✅ Conta criada! Redirecionando...</div>

      <div class="campo">
        <label>Nome completo</label>
        <input v-model="nome" type="text" placeholder="Seu nome" />
      </div>

      <div class="campo">
        <label>Email</label>
        <input v-model="email" type="email" placeholder="seu@email.com" />
      </div>

      <div class="campo">
        <label>Senha</label>
        <input v-model="senha" type="password" placeholder="mínimo 6 caracteres" />
      </div>

      <div class="campo">
        <label>Perfil</label>
        <select v-model="tipo">
          <option value="cliente">Cliente</option>
          <option value="cuidador">Cuidador</option>
        </select>
      </div>

      <button @click="cadastrar" :disabled="carregando">
        {{ carregando ? 'Cadastrando...' : 'Cadastrar' }}
      </button>

      <p class="link">
        Já tem conta?
        <a href="/">Entrar</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const nome = ref('')
const email = ref('')
const senha = ref('')
const tipo = ref('cliente')
const erro = ref('')
const sucesso = ref(false)
const carregando = ref(false)

async function cadastrar() {
  erro.value = ''

  if (!nome.value || !email.value || !senha.value) {
    erro.value = 'Preencha todos os campos'
    return
  }

  if (senha.value.length < 6) {
    erro.value = 'Senha deve ter no mínimo 6 caracteres'
    return
  }

  carregando.value = true
  try {
    await api.post('/usuarios/', {
      nome: nome.value,
      email: email.value,
      senha: senha.value,
      tipo: tipo.value,
    })
    sucesso.value = true
    setTimeout(() => router.push('/'), 2000)
  } catch (e: any) {
    erro.value = e.response?.data?.detail || 'Erro ao cadastrar'
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

input, select {
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

button:disabled {
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

.link {
  text-align: center;
  margin-top: 1rem;
  color: #718096;
}

.link a {
  color: #2c7a7b;
  font-weight: 500;
}
</style>