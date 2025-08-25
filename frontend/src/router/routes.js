const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Home.vue') },

      {
        path: 'teste-back',
        component: () => import('src/pages/TesteConexaoBack.vue')
      },

      {
    path: 'details/:id',   
    component: () => import('src/pages/EventoDetails.vue'),
    props: true
    }

    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
