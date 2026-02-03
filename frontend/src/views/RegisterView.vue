<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/auth/register', {
      email: email.value,
      password: password.value,
    })
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-container">
    <h1>Register</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          :disabled="loading"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          minlength="8"
          :disabled="loading"
        />
        <small>Minimum 8 characters</small>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <p class="auth-link">
      Already have an account? <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<style src="../auth.css"></style>
<style scoped>
small {
  color: #666;
  font-size: 0.85em;
}
</style>
