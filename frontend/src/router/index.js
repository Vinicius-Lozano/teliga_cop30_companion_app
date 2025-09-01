import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth' 

export default defineRouter(function () {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  // ✅ Proteção de rotas
  Router.beforeEach((to, from, next) => {
    const store = useAuthStore()

    // Verifica se a rota exige autenticação
    if (to.meta.requiresAuth && !store.isAuthenticated) {
      return next('/login')
    }

    // Verifica se a rota exige admin
    if (to.meta.requiresAdmin && (!store.user || !store.user.is_staff)) {
      return next('/') // manda pra Home se não for admin
    }

    next()
  })

  return Router
})
