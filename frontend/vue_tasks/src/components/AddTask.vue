<template>
  <form @submit.prevent="submitTask">
    <input
      v-model="title"
      type="text"
      placeholder="Название задачи"
      required
    />
    <label>
      <input type="checkbox" v-model="completed" />
      Выполнено
    </label>
    <button type="submit">Добавить задачу</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['task-added'])

const title = ref('')
const completed = ref(false)

async function submitTask() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title.value,
        completed: completed.value,
      }),
    })
    if (!res.ok) throw new Error('Ошибка при добавлении задачи')

    const newTask = await res.json()
    // Очистить форму
    title.value = ''
    completed.value = false

    alert('Задача добавлена!')
    emit('task-added', newTask) // уведомляем родителя, что задача добавлена
  } catch (error) {
    alert(error.message)
  }
}
</script>
