<template>
  <div id="app">
    <h1>Inventarverwaltung</h1>
    
    <section class="add-section">
      <h2>Neues Item</h2>
      <form @submit.prevent="createItem">
        <input v-model="newItem.name" placeholder="Name" required />
        <input v-model="newItem.category" placeholder="Kategorie" />
        <select v-model="newItem.status" required>
          <option value="">Status wählen</option>
          <option value="verfügbar">verfügbar</option>
          <option value="in Verwendung">in Verwendung</option>
          <option value="Wartung">Wartung</option>
        </select>
        <input v-model="newItem.location" placeholder="Ort" />
        <input v-model="newItem.assigned_to" placeholder="Zugewiesen an" />
        <button type="submit">Anlegen</button>
      </form>
    </section>

    <section class="list-section">
      <h2>Items</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Kategorie</th>
            <th>Status</th>
            <th>Ort</th>
            <th>Zugewiesen an</th>
            <th>Aktionen</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.status }}</td>
            <td>{{ item.location }}</td>
            <td>{{ item.assigned_to }}</td>
            <td>
              <button @click="deleteItem(item.id)">Löschen</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const items = ref([])
const newItem = ref({
  name: '',
  category: '',
  status: '',
  location: '',
  assigned_to: ''
})

async function loadItems() {
  try {
    const response = await axios.get(`${API_URL}/items`)
    items.value = response.data
  } catch (error) {
    console.error('Fehler beim Laden:', error)
  }
}

async function createItem() {
  try {
    await axios.post(`${API_URL}/items`, newItem.value)
    newItem.value = { name: '', category: '', status: '', location: '', assigned_to: '' }
    loadItems()
  } catch (error) {
    console.error('Fehler beim Erstellen:', error)
  }
}

async function deleteItem(id) {
  try {
    await axios.delete(`${API_URL}/items/${id}`)
    loadItems()
  } catch (error) {
    console.error('Fehler beim Löschen:', error)
  }
}

onMounted(() => {
  loadItems()
})
</script>

<style scoped>
#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
}

.add-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

form {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

input, select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
  min-width: 150px;
}

button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f8f9fa;
  font-weight: bold;
}

tr:hover {
  background: #f5f5f5;
}
</style>
