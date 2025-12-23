<script setup>
import { ref, computed, onMounted } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'
const todos = ref([])
const newTodoTitle = ref('')
const filter = ref('all') // 'all', 'active', 'completed'

async function fetchTodos() {
  try {
    const response = await fetch(`${API_URL}/`)
    const data = await response.json()
    todos.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Error fetching todos:', error)
    todos.value = []
  }
}

async function addTodo() {
  if (!newTodoTitle.value.trim()) return
  
  try {
    const response = await fetch(`${API_URL}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: newTodoTitle.value, done: false })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const newTodo = await response.json()
    todos.value.push(newTodo)
    newTodoTitle.value = ''
  } catch (error) {
    console.error('Error adding todo:', error)
  }
}

async function toggleTodo(todo) {
  try {
    const response = await fetch(`${API_URL}/${todo.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        task: todo.task,
        done: !todo.done 
      })
    })
    
    const updated = await response.json()
    const index = todos.value.findIndex(t => t.id === todo.id)
    todos.value[index] = updated
  } catch (error) {
    console.error('Error updating todo:', error)
  }
}

async function deleteTodo(id) {
  try {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    todos.value = todos.value.filter(t => t.id !== id)
  } catch (error) {
    console.error('Error deleting todo:', error)
  }
}

const filteredTodos = computed(() => {
  if (filter.value === 'active') {
    return todos.value.filter(t => !t.done)
  } else if (filter.value === 'completed') {
    return todos.value.filter(t => t.done)
  }
  return todos.value
})

const activeCount = computed(() => todos.value.filter(t => !t.done).length)
const completedCount = computed(() => todos.value.filter(t => t.done).length)

onMounted(fetchTodos)
</script>

<template>
  <div class="container">
    <h1>Todo App</h1>
    
    <div class="input-group">
      <input 
        v-model="newTodoTitle" 
        @keyup.enter="addTodo"
        placeholder="Введите новую задачу..."
        class="todo-input"
      />
      <button @click="addTodo" class="add-btn">Добавить</button>
    </div>

    <div class="filters">
      <button 
        @click="filter = 'all'" 
        :class="['filter-btn', { active: filter === 'all' }]"
      >
        Все ({{ todos.length }})
      </button>
      <button 
        @click="filter = 'active'" 
        :class="['filter-btn', { active: filter === 'active' }]"
      >
        Активные ({{ activeCount }})
      </button>
      <button 
        @click="filter = 'completed'" 
        :class="['filter-btn', { active: filter === 'completed' }]"
      >
        Завершённые ({{ completedCount }})
      </button>
    </div>

    <div v-if="filteredTodos.length === 0" class="empty-state">
      <p v-if="filter === 'all'">Нет задач. Добавьте первую!</p>
      <p v-else-if="filter === 'active'">Нет активных задач! 🎉</p>
      <p v-else>Нет завершённых задач</p>
    </div>

    <ul v-else class="todo-list">
      <li v-for="todo in filteredTodos" :key="todo.id" class="todo-item">
        <input 
          type="checkbox" 
          :checked="todo.done"
          @change="toggleTodo(todo)"
          class="checkbox"
        />
        <span :class="{ completed: todo.done }">{{ todo.task }}</span>
        <button @click="deleteTodo(todo.id)" class="delete-btn">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.todo-input {
  flex: 1;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.todo-input:focus {
  border-color: #4CAF50;
}

.add-btn {
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s;
}

.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  justify-content: center;
}

.filter-btn {
  padding: 10px 20px;
  background: #f0f0f0;
  color: #333;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.filter-btn:hover {
  background: #e0e0e0;
}

.filter-btn.active {
  background: #4CAF50;
  color: white;
  border-color: #45a049;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 18px;
}

.todo-list {
  list-style: none;
  padding: 0;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.todo-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.checkbox {
  width: 22px;
  height: 22px;
  cursor: pointer;
}

.todo-item span {
  flex: 1;
  font-size: 16px;
  transition: all 0.3s;
}

.completed {
  text-decoration: line-through;
  color: #999;
}

.delete-btn {
  padding: 6px 12px;
  background: none;
  color: #d00303;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 17px;
  transition: all 0.3s;
  opacity: 0.6;
}

/* .delete-btn:hover {
  opacity: 1;
  transform: scale(1.2);
} */
</style>
