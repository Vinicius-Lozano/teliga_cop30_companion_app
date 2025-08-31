const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/MapaPage.vue') },
      { path: 'login/', component: () => import('pages/LoginPage.vue') },
      { path: 'register', component: () => import('pages/Register.vue') },
      { path: 'details/:id', component: () => import('pages/EventoDetails.vue'), props: true},
      { path: 'item/:id', component: () => import('pages/ItemDetails.vue'), props: true },
      { path: 'teste-back', component: () => import('pages/TesteConexaoBack.vue')}
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
