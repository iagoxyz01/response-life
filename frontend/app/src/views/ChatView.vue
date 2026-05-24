 <template>
  <div class="container">
    <!-- Header -->
    <div class="chat-header">
      <div class="status-bar">
        <span>9:41</span>
        <div>📶 🔋</div>
      </div>
      <div class="header-content">
        <button class="back-btn" @click="voltar">←</button>
        <div class="avatar">💬</div>
        <div class="header-info">
          <div class="header-name">Chat</div>
          <div class="header-status">Online</div>
        </div>
      </div>
    </div>

    <!-- Mensagens -->
    <div class="messages-container" ref="messagesContainer">
      <div v-if="mensagens.length === 0" class="empty-chat">
        <div class="empty-icon">💬</div>
        <div class="empty-text">Nenhuma mensagem ainda</div>
        <div class="empty-sub">Inicie uma conversa!</div>
      </div>

      <div
        v-for="msg in mensagens"
        :key="msg.id"
        class="message-wrapper"
        :class="{ 'own': msg.proprio }"
      >
        <div class="message" :class="{ 'message-own': msg.proprio }">
          <div class="message-text">{{ msg.texto }}</div>
          <div class="message-time">{{ msg.hora }}</div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="input-container">
      <input
        v-model="textoMensagem"
        placeholder="Digite uma mensagem..."
        @keyup.enter="enviarMensagem"
        class="message-input"
      />
      <button class="send-btn" @click="enviarMensagem">
        ➤
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const mensagens = ref<any[]>([])
const textoMensagem = ref('')
const messagesContainer = ref<HTMLElement>()
let ws: WebSocket | null = null

const usuarioId = 1 // Temporário — vamos pegar do token depois
const roomId = 'sala-geral' // Sala geral por enquanto

onMounted(() => {
  conectarWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})

function conectarWebSocket() {
  const wsUrl = `ws://127.0.0.1:8000/chat/ws/${roomId}/${usuarioId}`
  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket conectado!')
  }

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    mensagens.value.push({
      id: Date.now(),
      texto: data.texto,
      proprio: data.usuario_id === usuarioId,
      hora: new Date().toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit',
      }),
    })
    scrollParaBaixo()
  }

  ws.onclose = () => {
    console.log('WebSocket desconectado')
  }
}

async function enviarMensagem() {
  if (!textoMensagem.value.trim() || !ws) return

  ws.send(JSON.stringify({
    texto: textoMensagem.value,
    usuario_id: usuarioId,
  }))

  textoMensagem.value = ''
}

async function scrollParaBaixo() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function voltar() {
  router.back()
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #f0f4f8;
  display: flex;
  flex-direction: column;
}

.chat-header {
  background: linear-gradient(135deg, #1a5c5c 0%, #2c7a7b 100%);
  padding: 0 16px 16px;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  padding: 36px 4px 8px;
  font-size: .7rem;
  color: rgba(255,255,255,.7);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-btn {
  background: rgba(255,255,255,.2);
  border: none;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 40px;
  height: 40px;
  background: rgba(255,255,255,.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.header-name {
  font-size: 1rem;
  font-weight: 700;
  color: white;
}

.header-status {
  font-size: .75rem;
  color: rgba(255,255,255,.75);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;
}

.empty-chat {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon { font-size: 3rem; margin-bottom: 12px; }
.empty-text { font-size: 1rem; font-weight: 600; color: #475569; }
.empty-sub { font-size: .85rem; color: #94a3b8; margin-top: 4px; }

.message-wrapper {
  display: flex;
  margin-bottom: 12px;
}

.message-wrapper.own {
  justify-content: flex-end;
}

.message {
  background: white;
  border-radius: 16px 16px 16px 4px;
  padding: 10px 14px;
  max-width: 75%;
  box-shadow: 0 1px 3px rgba(0,0,0,.08);
}

.message-own {
  background: #2c7a7b;
  border-radius: 16px 16px 4px 16px;
}

.message-text {
  font-size: .9rem;
  color: #0f172a;
  line-height: 1.4;
}

.message-own .message-text {
  color: white;
}

.message-time {
  font-size: .65rem;
  color: #94a3b8;
  margin-top: 4px;
  text-align: right;
}

.message-own .message-time {
  color: rgba(255,255,255,.7);
}

.input-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 12px 16px 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 10px;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: .75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  font-size: .9rem;
  outline: none;
  background: #f8faff;
}

.message-input:focus {
  border-color: #2c7a7b;
}

.send-btn {
  width: 44px;
  height: 44px;
  background: #2c7a7b;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
