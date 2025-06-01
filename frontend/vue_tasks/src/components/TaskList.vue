<template>
  <div class="task-list">
    <h2>Список задач</h2>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} - <strong>{{ task.completed ? 'Выполнено' : 'В процессе' }}</strong>
        <button @click="deleteTask(task.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  tasks: Array
})

const emit = defineEmits(['task-deleted'])

const deleteTask = async (id) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
      method: 'DELETE',
    })

    if (res.ok) {
      emit('task-deleted', id) // уведомляем родителя
    } else {
      const err = await res.json()
      console.error('Ошибка при удалении:', err)
    }
  } catch (err) {
    console.error('Ошибка при удалении:', err)
  }
}
</script>

<style scoped>
button {
  margin-left: 1rem;
  color: white;
  background-color: red;
  border: none;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
</style>
