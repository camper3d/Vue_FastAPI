<template>
  <div class="bg-white p-6 rounded-xl shadow space-y-4">
    <h2 class="text-xl font-semibold">Список задач</h2>
    <ul class="grid gap-4 sm:grid-cols-1 md:grid-cols-2">
      <li
        v-for="task in tasks"
        :key="task.id"
        class="flex justify-between items-center border p-4 rounded hover:shadow transition bg-gray-50"
      >
        <div>
          <p class="font-medium">{{ task.title }}</p>
          <p class="text-sm text-gray-600">
            {{ task.completed ? '✅ Выполнено' : '⌛ В процессе' }}
          </p>
        </div>
        <button
          @click="deleteTask(task.id)"
          class="text-red-600 hover:text-red-800 font-semibold"
        >
          Удалить
        </button>
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
      emit('task-deleted', id)
    } else {
      const err = await res.json()
      console.error('Ошибка при удалении:', err)
    }
  } catch (err) {
    console.error('Ошибка при удалении:', err)
  }
}
</script>