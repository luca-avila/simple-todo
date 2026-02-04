<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const tasks = ref([])
const newTaskTitle = ref('')
const newTaskDescription = ref('')
const error = ref('')
const loading = ref(false)
const adding = ref(false)

async function fetchTasks() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.get('/tasks/')
    tasks.value = response.data.items
  } catch (e) {
    if (e.response?.status === 401) {
      router.push('/login')
    } else {
      error.value = 'Failed to fetch tasks'
    }
  } finally {
    loading.value = false
  }
}

async function addTask() {
  if (!newTaskTitle.value.trim()) return
  adding.value = true
  error.value = ''
  try {
    const payload = { title: newTaskTitle.value }
    if (newTaskDescription.value.trim()) {
      payload.description = newTaskDescription.value
    }
    const response = await api.post('/tasks/', payload)
    tasks.value.push(response.data)
    newTaskTitle.value = ''
    newTaskDescription.value = ''
  } catch (e) {
    error.value = 'Failed to add task'
  } finally {
    adding.value = false
  }
}

async function toggleComplete(task) {
  error.value = ''
  try {
    const response = await api.patch(`/tasks/${task.id}`, { completed: !task.completed })
    task.completed = response.data.completed
  } catch (e) {
    error.value = 'Failed to update task'
  }
}

async function deleteTask(task) {
  error.value = ''
  try {
    await api.delete(`/tasks/${task.id}`)
    tasks.value = tasks.value.filter(t => t.id !== task.id)
  } catch (e) {
    error.value = 'Failed to delete task'
  }
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}

onMounted(fetchTasks)
</script>

<template>
  <div class="task-container">
    <div class="header">
      <h1>My Tasks</h1>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>

    <form class="add-form" @submit.prevent="addTask">
      <input
        v-model="newTaskTitle"
        type="text"
        placeholder="Task title..."
        required
        :disabled="adding"
      />
      <input
        v-model="newTaskDescription"
        type="text"
        placeholder="Description (optional)"
        :disabled="adding"
      />
      <button type="submit" :disabled="adding">
        {{ adding ? 'Adding...' : 'Add' }}
      </button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>

    <p v-if="loading" class="loading">Loading tasks...</p>

    <ul v-else class="task-list">
      <li v-for="task in tasks" :key="task.id" class="task-item">
        <input
          type="checkbox"
          :checked="task.completed"
          @change="toggleComplete(task)"
        />
        <div class="task-content" :class="{ completed: task.completed }">
          <span class="task-title">{{ task.title }}</span>
          <span v-if="task.description" class="task-description">{{ task.description }}</span>
        </div>
        <button class="delete-btn" @click="deleteTask(task)">Delete</button>
      </li>
    </ul>

    <p v-if="!loading && tasks.length === 0" class="empty">No tasks yet</p>
  </div>
</template>

<style scoped>
.task-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logout-btn {
  padding: 8px 16px;
  background: #666;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.add-form input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-form button {
  padding: 8px 16px;
  background: #333;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-list {
  list-style: none;
  padding: 0;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.task-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.task-content.completed {
  text-decoration: line-through;
  color: #888;
}

.task-description {
  font-size: 0.85em;
  color: #666;
}

.delete-btn {
  padding: 4px 8px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error {
  color: red;
  margin-bottom: 10px;
}

.empty {
  text-align: center;
  color: #888;
}

.loading {
  text-align: center;
  color: #666;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

input:disabled {
  background: #f5f5f5;
}
</style>
