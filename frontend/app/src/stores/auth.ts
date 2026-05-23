import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    tipo: localStorage.getItem('tipo') || '',
  }),

  getters: {
    isLogado: (state) => !!state.token,
    isCliente: (state) => state.tipo === 'cliente',
    isCuidador: (state) => state.tipo === 'cuidador',
  },

  actions: {
    async login(email: string, senha: string) {
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', senha)

      console.log('Tentando login...', email)

      try {
        const response = await api.post('/usuarios/login', formData)
        console.log('Resposta:', response.data)
        const token = response.data.access_token

        this.token = token
        localStorage.setItem('token', token)

        const payload = JSON.parse(atob(token.split('.')[1]))
        this.tipo = payload.tipo
        localStorage.setItem('tipo', payload.tipo)
      } catch (error) {
        console.error('Erro no login:', error)
        throw error
      }
    },

    logout() {
      this.token = ''
      this.tipo = ''
      localStorage.removeItem('token')
      localStorage.removeItem('tipo')
    },
  },
})