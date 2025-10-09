const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/MapaPage.vue') },
      { path: 'login/', component: () => import('pages/LoginPage.vue') },
      { path: 'register', component: () => import('pages/Register.vue') },
      { path: 'details/:id', component: () => import('pages/EventoDetails.vue'), props: true },

      
      { path: 'item/:id', name:'ItemDetalhes', component: () => import('pages/ItemDetails.vue'), props: true },
      { path: 'item/:id/captura', name: 'PaginaDeCaptura', component: () => import('pages/CapturaPage.vue')},
      { path: 'mochila', component: () => import('src/pages/MochilaPage.vue')},

      { path: 'teste-back', component: () => import('pages/TesteConexaoBack.vue') },
      {
        path: 'admin/eventos',
        component: () => import('pages/AdminEventos.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'profile',
        component: () => import('pages/ProfilePage.vue'),
        meta: { requiresAuth: true } 
      }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes

