<template>
  <nav class="bottom-nav">
    <div
      class="bnav-item"
      :class="{ active: rota === 'home' }"
      @click="ir('home')"
    >
      <span class="icon">🏠</span>
      <span class="label">Home</span>
    </div>
    <div
      class="bnav-item"
      :class="{ active: rota === 'chat' }"
      @click="ir('chat')"
    >
      <span class="icon">💬</span>
      <span class="label">Chat</span>
    </div>
    <div
      class="bnav-item"
      :class="{ active: rota === 'historico' }"
      @click="ir('historico')"
    >
      <span class="icon">📂</span>
      <span class="label">Histórico</span>
    </div>
    <div
      class="bnav-item"
      :class="{ active: rota === 'carteira' }"
      @click="ir('carteira')"
    >
      <span class="icon">💰</span>
      <span class="label">Carteira</span>
    </div>
    <div
      class="bnav-item"
      :class="{ active: rota === 'perfil' }"
      @click="ir('perfil')"
    >
      <span class="icon">👤</span>
      <span class="label">Perfil</span>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const rota = computed(() => {
  const path = route.path
  if (path.includes('home')) return 'home'
  if (path.includes('chat')) return 'chat'
  if (path.includes('historico')) return 'historico'
  if (path.includes('carteira')) return 'carteira'
  if (path.includes('perfil')) return 'perfil'
  return ''
})

function ir(destino: string) {
  if (destino === 'home') {
    router.push(authStore.isCliente ? '/home-cliente' : '/home-cuidador')
  } else {
    router.push(`/${destino}`)
  }
}
</script>

<style scoped>
.bottom-nav {
  display: flex;
  justify-content: space-around;
  padding: 10px 8px 16px;
  border-top: 1px solid #e2e8f0;
  background: white;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.bnav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 12px;
  transition: all 0.2s;
}

.bnav-item:hover,
.bnav-item.active {
  background: #e6f4f4;
}

.icon {
  font-size: 1.2rem;
}

.label {
  font-size: 0.6rem;
  font-weight: 600;
  color: #94a3b8;
}

.bnav-item.active .label {
  color: #2c7a7b;
}
</style>