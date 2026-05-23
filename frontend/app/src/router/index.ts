import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/home-cliente',
      name: 'home-cliente',
      component: () => import('../views/HomeClienteView.vue'),
    },
    {
      path: '/home-cuidador',
      name: 'home-cuidador',
      component: () => import('../views/HomeCuidadorView.vue'),
    },
    {
      path: '/cadastro',
      name: 'cadastro',
      component: () => import('../views/CadastroView.vue'),
    },
    {
      path: '/agendamento',
      name: 'agendamento',
      component: () => import('../views/AgendamentoView.vue'),
    },
    {
      path: '/historico',
      name: 'historico',
      component: () => import('../views/HistoricoView.vue'),
    },
    {
      path: '/cadastro-servico',
      name: 'cadastro-servico',
      component: () => import('../views/CadastroServicoView.vue'),
    },
    {
  path: '/avaliacao/:id',
  name: 'avaliacao',
  component: () => import('../views/AvaliacaoView.vue'),
},
{
  path: '/recuperar-senha',
  name: 'recuperar-senha',
  component: () => import('../views/RecuperarSenhaView.vue'),
},
{
  path: '/nova-senha',
  name: 'nova-senha',
  component: () => import('../views/NovaSenhaView.vue'),
},
  ],
})

export default router

