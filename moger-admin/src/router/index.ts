import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import { userLoggedIn } from '@/utils/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'loginPage',
      component: LoginView,
      meta: { requiresAuth: false }
    }
  ]
})

router.beforeEach(async (to, from) => {
  if (to.meta.requiresAuth && !(await userLoggedIn())) {
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }
})
export default router
