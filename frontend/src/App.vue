<script setup>
import { ref, onMounted } from 'vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const todos = ref([])
const newTodoTitle = ref('')

async function fetchTodos() {
  try {
    const response = await fetch(`${API_URL}/`)
    todos.value = await response.json()
  } catch (error) {
    console.error('Error fetching todos:', error)
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

    <div v-if="todos.length === 0" class="empty-state">
      <p>Нет задач. Добавьте первую!</p>
    </div>

    <ul v-else class="todo-list">
      <li v-for="todo in todos" :key="todo.id" class="todo-item">
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

.add-btn:hover {
  background: #45a049;
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
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.3s, transform 0.2s;
}

.delete-btn:hover {
  opacity: 1;
  transform: scale(1.2);
}
</style>
