import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import TaskListView from '../views/TaskListView.vue'

const routes = [
  { path: '/', redirect: '/tasks' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/tasks', component: TaskListView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

function isTokenExpired(token) {
  if (!token) return true
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token')
    if (!token || isTokenExpired(token)) {
      return '/login'
    }
  }
})

export default router
