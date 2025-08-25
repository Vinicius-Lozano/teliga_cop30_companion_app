const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Home.vue') },
      { path: 'login/', component: () => import('pages/LoginPage.vue') },
      { path: 'details/:id', component: () => import('pages/Details.vue') },
      { path: 'teste-back', component: () => import('pages/TesteConexaoBack.vue')},
      { path: 'register', component: () => import('pages/Register.vue') }
    ]
  },

  
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes