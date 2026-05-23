 
<template>
  <div class="container">
    <div class="card">
      <h1>Response Life</h1>
      <p class="subtitle">Conectando cuidadores e clientes</p>

      <div v-if="erro" class="erro">{{ erro }}</div>

      <form @submit.prevent="entrar">
        <div class="campo">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="seu@email.com"
            required
          />
        </div>

        <div class="campo">
          <label>Senha</label>
          <input
            v-model="senha"
            type="password"
            placeholder="sua senha"
            required
          />
        </div>

        <button type="submit" :disabled="carregando">
          {{ carregando ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>

      <p class="link">
        Não tem conta?
        <a href="/cadastro">Cadastre-se</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const senha = ref('')
const erro = ref('')
const carregando = ref(false)

async function entrar() {
  erro.value = ''
  carregando.value = true
  try {
    await authStore.login(email.value, senha.value)
    if (authStore.isCliente) {
      router.push('/home-cliente')
    } else {
      router.push('/home-cuidador')
    }
  } catch (e: any) {
    erro.value = 'Email ou senha inválidos'
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
  margin-bottom: 2rem;
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
  margin-top: 1rem;
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