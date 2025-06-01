<template>
  <div>
    <AddTask @task-added="fetchTasks" />
    <TaskList
      :tasks="tasks"
      @task-deleted="removeTask"
      @task-updated="updateTask"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AddTask from './components/AddTask.vue'
import TaskList from './components/TaskList.vue'

const tasks = ref([])

async function fetchTasks() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/tasks')
    if (!res.ok) throw new Error('Ошибка при загрузке задач')
    tasks.value = await res.json()
  } catch (error) {
    alert(error.message)
  }
}

const removeTask = (id) => {
  tasks.value = tasks.value.filter(t => t.id !== id)
}

const updateTask = (updatedTask) => {
  const index = tasks.value.findIndex(t => t.id === updatedTask.id)
  if (index !== -1) {
    tasks.value[index] = updatedTask
  }
}

onMounted(fetchTasks)
</script>
