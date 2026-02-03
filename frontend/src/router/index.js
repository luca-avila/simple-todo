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

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !localStorage.getItem('access_token')) {
    return '/login'
  }
})

export default router
