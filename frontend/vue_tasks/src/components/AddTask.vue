<template>
  <form @submit.prevent="submitTask" class="flex flex-col space-y-4 bg-white p-6 rounded-xl shadow">
    <input
      v-model="title"
      type="text"
      placeholder="Название задачи"
      required
      class="border p-2 rounded w-full"
    />
    <label class="inline-flex items-center space-x-2">
      <input type="checkbox" v-model="completed" class="accent-blue-500" />
      <span>Выполнено</span>
    </label>
    <button
      type="submit"
      class="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
    >
      Добавить задачу
    </button>
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
    title.value = ''
    completed.value = false
    emit('task-added', newTask)
  } catch (error) {
    alert(error.message)
  }
}
</script>

