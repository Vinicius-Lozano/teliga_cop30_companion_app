const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Home.vue') },
      { path: 'details/:id', component: () => import('pages/Details.vue') },
      {path: 'teste-back', component: () => import('src/pages/TesteConexaoBack.vue')}
    ]
  },

  
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes