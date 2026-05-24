<template>
  <div class="container">
    <!-- Header -->
    <div class="hero-header">
      <div class="status-bar">
        <span>9:41</span>
        <div>📶 🔋</div>
      </div>
      <div class="hero-greeting">Olá, Cuidador 👋</div>
      <div class="hero-sub">Seus atendimentos de hoje</div>
      <div class="hero-stats">
        <div class="stat-card">
          <div class="stat-num">{{ totalAtendimentos }}</div>
          <div class="stat-label">Total</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">{{ pendentes }}</div>
          <div class="stat-label">Pendentes</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">{{ concluidos }}</div>
          <div class="stat-label">Concluídos</div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="scroll-content">
      <div class="section-label">Ações Rápidas</div>

      <div class="action-grid">
        <div class="action-card" @click="ir('/cadastro-servico')">
          <div class="action-icon">➕</div>
          <div class="action-title">Novo Serviço</div>
          <div class="action-sub">Cadastrar serviço</div>
        </div>
        <div class="action-card" @click="ir('/chat')">
          <div class="action-icon">💬</div>
          <div class="action-title">Chat</div>
          <div class="action-sub">Falar com cliente</div>
        </div>
        <div class="action-card" @click="ir('/monitoramento')">
          <div class="action-icon">📸</div>
          <div class="action-title">Monitoramento</div>
          <div class="action-sub">Enviar fotos</div>
        </div>
        <div class="action-card" @click="ir('/carteira')">
          <div class="action-icon">💰</div>
          <div class="action-title">Carteira</div>
          <div class="action-sub">Ver saldo</div>
        </div>
      </div>

      <div class="section-label">Próximos Atendimentos</div>

      <div v-if="agendamentos.length === 0" class="empty-card">
        <div class="empty-icon">📭</div>
        <div class="empty-text">Nenhum atendimento pendente</div>
      </div>

      <div
        v-for="ag in agendamentos"
        :key="ag.id"
        class="agendamento-card"
      >
        <div class="ag-icon">👤</div>
        <div class="ag-info">
          <div class="ag-title">Cliente #{{ ag.cliente_id }}</div>
          <div class="ag-date">📅 {{ formatarData(ag.data_inicio) }}</div>
        </div>
        <div class="ag-actions">
          <span class="tag tag-amber" v-if="ag.status === 'pendente'">Pendente</span>
          <button
            v-if="ag.status === 'pendente'"
            class="btn-concluir"
            @click="concluir(ag.id)"
          >
            ✓ Concluir
          </button>
        </div>
      </div>
    </div>

    <BottomNav />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import BottomNav from '../components/BottomNav.vue'

const router = useRouter()
const agendamentos = ref<any[]>([])

const totalAtendimentos = computed(() => agendamentos.value.length)
const pendentes = computed(() => agendamentos.value.filter(a => a.status === 'pendente').length)
const concluidos = computed(() => agendamentos.value.filter(a => a.status === 'concluido').length)

onMounted(async () => {
  try {
    const response = await api.get('/agendamentos/meus')
    agendamentos.value = response.data.filter((a: any) => a.status === 'pendente')
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

async function concluir(id: number) {
  try {
    await api.patch(`/agendamentos/${id}/concluir`)
    agendamentos.value = agendamentos.value.filter(a => a.id !== id)
  } catch (e) {
    console.error(e)
  }
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
  top: -40px; right: -40px;
  width: 160px; height: 160px;
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
  gap: 10px;
}

.stat-card {
  background: rgba(255,255,255,.15);
  border-radius: 12px;
  padding: 10px 12px;
  flex: 1;
  text-align: center;
}

.stat-num {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
}

.stat-label {
  font-size: .65rem;
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

.action-icon { font-size: 1.5rem; margin-bottom: 8px; }
.action-title { font-size: .85rem; font-weight: 700; color: #0f172a; }
.action-sub { font-size: .72rem; color: #94a3b8; }

.empty-card {
  background: white;
  border-radius: 16px;
  padding: 32px 16px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.empty-icon { font-size: 2rem; margin-bottom: 8px; }
.empty-text { color: #94a3b8; font-size: .85rem; }

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
  width: 44px; height: 44px;
  background: #e6f4f4;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ag-info { flex: 1; }
.ag-title { font-size: .85rem; font-weight: 700; color: #0f172a; }
.ag-date { font-size: .75rem; color: #94a3b8; }

.ag-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.tag {
  padding: .25rem .75rem;
  border-radius: 20px;
  font-size: .72rem;
  font-weight: 600;
}

.tag-amber { background: #fef3c7; color: #92400e; }

.btn-concluir {
  background: #2c7a7b;
  color: white;
  border: none;
  padding: .3rem .8rem;
  border-radius: 20px;
  font-size: .75rem;
  cursor: pointer;
  font-weight: 600;
}
</style>