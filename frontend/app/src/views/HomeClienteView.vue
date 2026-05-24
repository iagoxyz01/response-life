<template>
  <div class="container">
    <!-- Header -->
    <div class="hero-header">
      <div class="status-bar">
        <span>9:41</span>
        <div>📶 🔋</div>
      </div>
      <div class="hero-content">
        <div class="hero-greeting">Olá, {{ nomeUsuario }} 👋</div>
        <div class="hero-sub">Como podemos ajudar hoje?</div>
      </div>
      <div class="hero-stats">
        <div class="stat-card">
          <div class="stat-num">{{ totalAgendamentos }}</div>
          <div class="stat-label">Agendamentos</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">{{ pendentes }}</div>
          <div class="stat-label">Pendentes</div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="scroll-content">
      <div class="section-label">Ações Rápidas</div>

      <div class="action-grid">
        <div class="action-card" @click="ir('/agendamento')">
          <div class="action-icon">📅</div>
          <div class="action-title">Novo Agendamento</div>
          <div class="action-sub">Agendar cuidador</div>
        </div>
        <div class="action-card" @click="ir('/historico')">
          <div class="action-icon">📂</div>
          <div class="action-title">Histórico</div>
          <div class="action-sub">Ver atendimentos</div>
        </div>
        <div class="action-card" @click="ir('/chat')">
          <div class="action-icon">💬</div>
          <div class="action-title">Chat</div>
          <div class="action-sub">Falar com cuidador</div>
        </div>
        <div class="action-card" @click="ir('/carteira')">
          <div class="action-icon">💰</div>
          <div class="action-title">Carteira</div>
          <div class="action-sub">Pagamentos</div>
        </div>
      </div>

      <div class="section-label">Próximos Agendamentos</div>

      <div v-if="proximosAgendamentos.length === 0" class="empty-card">
        <div class="empty-icon">📭</div>
        <div class="empty-text">Nenhum agendamento pendente</div>
        <button class="btn-primary" @click="ir('/agendamento')">Agendar agora</button>
      </div>

      <div
        v-for="ag in proximosAgendamentos"
        :key="ag.id"
        class="agendamento-card"
      >
        <div class="ag-icon">🩺</div>
        <div class="ag-info">
          <div class="ag-title">Serviço #{{ ag.servico_id }}</div>
          <div class="ag-date">📅 {{ formatarData(ag.data_inicio) }}</div>
        </div>
        <span class="tag tag-amber">{{ ag.status }}</span>
      </div>
    </div>

    <!-- Bottom Nav -->
    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'
import BottomNav from '../components/BottomNav.vue'

const router = useRouter()
const authStore = useAuthStore()

const nomeUsuario = ref('Cliente')
const agendamentos = ref<any[]>([])

const totalAgendamentos = computed(() => agendamentos.value.length)
const pendentes = computed(() => agendamentos.value.filter(a => a.status === 'pendente').length)
const proximosAgendamentos = computed(() => agendamentos.value.filter(a => a.status === 'pendente'))

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
    hour: '2-digit',
    minute: '2-digit',
  })
}

function ir(rota: string) {
  router.push(rota)
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f0f4f8;
  padding-bottom: 80px;
}

.hero-header {
  background: linear-gradient(135deg, #1a5c5c 0%, #2c7a7b 60%, #3d9a9b 100%);
  padding: 0 16px 24px;
  position: relative;
  overflow: hidden;
}

.hero-header::before {
  content: '';
  position: absolute;
  top: -40px;
  right: -40px;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: rgba(255,255,255,.08);
}

.status-bar {
  display: flex;
  justify-content: space-between;
  padding: 36px 4px 8px;
  font-size: .7rem;
  font-weight: 600;
  color: rgba(255,255,255,.7);
}

.hero-greeting {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.hero-sub {
  font-size: .85rem;
  color: rgba(255,255,255,.75);
  margin-bottom: 16px;
}

.hero-stats {
  display: flex;
  gap: 12px;
}

.stat-card {
  background: rgba(255,255,255,.15);
  border-radius: 12px;
  padding: 10px 16px;
  flex: 1;
  text-align: center;
}

.stat-num {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
}

.stat-label {
  font-size: .7rem;
  color: rgba(255,255,255,.75);
}

.scroll-content {
  padding: 16px;
}

.section-label {
  font-size: .7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: #94a3b8;
  margin: 16px 0 10px;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 8px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.08);
  cursor: pointer;
  transition: all .2s;
  border: 1px solid #e2e8f0;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(44,122,123,.15);
}

.action-icon {
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.action-title {
  font-size: .85rem;
  font-weight: 700;
  color: #0f172a;
}

.action-sub {
  font-size: .72rem;
  color: #94a3b8;
}

.empty-card {
  background: white;
  border-radius: 16px;
  padding: 32px 16px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.empty-text {
  color: #94a3b8;
  font-size: .85rem;
  margin-bottom: 16px;
}

.btn-primary {
  background: #2c7a7b;
  color: white;
  border: none;
  padding: .6rem 1.2rem;
  border-radius: 20px;
  font-size: .85rem;
  cursor: pointer;
  font-weight: 600;
}

.agendamento-card {
  background: white;
  border-radius: 16px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}

.ag-icon {
  font-size: 1.5rem;
  width: 44px;
  height: 44px;
  background: #e6f4f4;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ag-info {
  flex: 1;
}

.ag-title {
  font-size: .85rem;
  font-weight: 700;
  color: #0f172a;
}

.ag-date {
  font-size: .75rem;
  color: #94a3b8;
}

.tag {
  padding: .25rem .75rem;
  border-radius: 20px;
  font-size: .72rem;
  font-weight: 600;
}

.tag-amber {
  background: #fef3c7;
  color: #92400e;
}
</style>