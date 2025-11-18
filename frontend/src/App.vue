<template>
  <div class="app-container">
    <!-- Animated Background Grid -->
    <div class="grid-background"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header with Glow Effect -->
      <header class="header">
        <div class="header-content">
          <div class="logo-section">
            <div class="logo-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
              </svg>
            </div>
            <h1 class="title">Inventarverwaltung</h1>
          </div>
          <div class="stats-section">
            <div class="stat-card">
              <span class="stat-label">Gesamt</span>
              <span class="stat-value">{{ items.length }}</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">Verfügbar</span>
              <span class="stat-value">{{ availableCount }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Add Item Section with Glow Border -->
      <section class="add-section">
        <div class="section-header">
          <h2 class="section-title">Neues Item</h2>
          <div class="glow-line"></div>
        </div>
        <form @submit.prevent="createItem" class="add-form">
          <div class="input-group">
            <input 
              v-model="newItem.name" 
              placeholder="Name" 
              required 
              class="glow-input"
            />
          </div>
          <div class="input-group">
            <input 
              v-model="newItem.category" 
              placeholder="Kategorie" 
              class="glow-input"
            />
          </div>
          <div class="input-group">
            <select v-model="newItem.status" required class="glow-select">
              <option value="">Status wählen</option>
              <option value="verfügbar">✓ Verfügbar</option>
              <option value="in Verwendung">⚡ In Verwendung</option>
              <option value="Wartung">🔧 Wartung</option>
            </select>
          </div>
          <div class="input-group">
            <input 
              v-model="newItem.location" 
              placeholder="Ort" 
              class="glow-input"
            />
          </div>
          <div class="input-group">
            <input 
              v-model="newItem.assigned_to" 
              placeholder="Zugewiesen an" 
              class="glow-input"
            />
          </div>
          <button type="submit" class="shimmer-button">
            <span class="shimmer-button-content">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              Item hinzufügen
            </span>
            <div class="shimmer"></div>
          </button>
        </form>
      </section>

      <!-- Items Grid with Card Spotlight -->
      <section class="items-section">
        <div class="section-header">
          <h2 class="section-title">Inventar</h2>
          <div class="glow-line"></div>
        </div>
        <div class="items-grid">
          <div 
            v-for="item in items" 
            :key="item.id" 
            class="item-card"
            @mouseenter="hoveredCard = item.id"
            @mouseleave="hoveredCard = null"
          >
            <div class="card-spotlight" :class="{ active: hoveredCard === item.id }"></div>
            <div class="card-content">
              <div class="card-header">
                <div class="item-id">#{{ item.id }}</div>
                <div class="status-badge" :class="getStatusClass(item.status)">
                  {{ item.status }}
                </div>
              </div>
              <h3 class="item-name">{{ item.name }}</h3>
              <div class="item-details">
                <div class="detail-row">
                  <span class="detail-label">Kategorie</span>
                  <span class="detail-value">{{ item.category || '-' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Ort</span>
                  <span class="detail-value">{{ item.location || '-' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Zugewiesen</span>
                  <span class="detail-value">{{ item.assigned_to || '-' }}</span>
                </div>
              </div>
              <button @click="deleteItem(item.id)" class="delete-button">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                Löschen
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const items = ref([])
const hoveredCard = ref(null)
const newItem = ref({
  name: '',
  category: '',
  status: '',
  location: '',
  assigned_to: ''
})

const availableCount = computed(() => {
  return items.value.filter(item => item.status === 'verfügbar').length
})

function getStatusClass(status) {
  const classes = {
    'verfügbar': 'status-available',
    'in Verwendung': 'status-in-use',
    'Wartung': 'status-maintenance'
  }
  return classes[status] || ''
}

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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  position: relative;
  overflow-x: hidden;
}

/* Animated Grid Background */
.grid-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.content-wrapper {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* Header Styles */
.header {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.logo-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stats-section {
  display: flex;
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Section Styles */
.add-section, .items-section {
  margin-bottom: 3rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  margin-bottom: 0.5rem;
}

.glow-line {
  height: 2px;
  width: 100px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}

/* Add Form Styles */
.add-form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.input-group {
  position: relative;
}

.glow-input, .glow-select {
  width: 100%;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  outline: none;
}

.glow-input:focus, .glow-select:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: #667eea;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}

.glow-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.glow-select option {
  background: #302b63;
  color: white;
}

/* Shimmer Button */
.shimmer-button {
  grid-column: 1 / -1;
  position: relative;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s ease;
}

.shimmer-button:hover {
  transform: translateY(-2px);
}

.shimmer-button:active {
  transform: translateY(0);
}

.shimmer-button-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.shimmer-button-content .icon {
  width: 20px;
  height: 20px;
}

.shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Items Grid */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

/* Item Card with Spotlight Effect */
.item-card {
  position: relative;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.item-card:hover {
  transform: translateY(-4px);
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.card-spotlight {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.15) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.card-spotlight.active {
  opacity: 1;
}

.card-content {
  position: relative;
  z-index: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.item-id {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-available {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-in-use {
  background: rgba(234, 179, 8, 0.2);
  color: #eab308;
  border: 1px solid rgba(234, 179, 8, 0.3);
}

.status-maintenance {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.item-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.detail-value {
  font-size: 0.875rem;
  color: white;
  font-weight: 500;
}

.delete-button {
  width: 100%;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.delete-button:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.delete-button svg {
  width: 16px;
  height: 16px;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .add-form {
    grid-template-columns: 1fr;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
}
</style>
