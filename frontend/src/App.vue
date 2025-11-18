<template>
  <div class="app-container">
    <!-- Decorative Frame Overlay -->
    <div class="frame-overlay"></div>

    <!-- Splash Screen -->
    <transition name="fade">
      <div v-if="showSplash" class="splash-screen">
        <h1 class="splash-title">Inventarverwaltung</h1>
      </div>
    </transition>

    <!-- Animated Background Grid -->
    <div class="grid-background"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper" :class="{ 'content-hidden': showSplash }">
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
            <select 
              v-model="newItem.category" 
              @change="handleCategoryChange"
              class="glow-select"
            >
              <option value="">Kategorie wählen</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              <option value="__ADD_NEW__">➕ Neue Kategorie hinzufügen...</option>
            </select>
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

    <!-- Modal: Neue Kategorie -->
    <transition name="modal">
      <div v-if="showCategoryModal" class="modal-backdrop" @click.self="closeCategoryModal">
        <div class="modal-content">
          <h3 class="modal-title">Neue Kategorie anlegen</h3>
          <input 
            v-model="newCategoryName" 
            @keyup.enter="addNewCategory"
            placeholder="Kategorie-Name eingeben" 
            class="glow-input modal-input"
            ref="categoryInput"
          />
          <div class="modal-actions">
            <button @click="addNewCategory" class="modal-button primary">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              Speichern
            </button>
            <button @click="closeCategoryModal" class="modal-button secondary">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              Abbrechen
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const items = ref([])
const hoveredCard = ref(null)
const showSplash = ref(true)
const showCategoryModal = ref(false)
const newCategoryName = ref('')
const categoryInput = ref(null)
const categories = ref(JSON.parse(localStorage.getItem('categories') || '["Hardware", "Software", "Möbel", "Zubehör"]'))

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

function handleCategoryChange() {
  if (newItem.value.category === '__ADD_NEW__') {
    newItem.value.category = ''
    showCategoryModal.value = true
    nextTick(() => {
      categoryInput.value?.focus()
    })
  }
}

function closeCategoryModal() {
  showCategoryModal.value = false
  newCategoryName.value = ''
}

function addNewCategory() {
  const trimmed = newCategoryName.value.trim()
  if (trimmed && !categories.value.includes(trimmed)) {
    categories.value.push(trimmed)
    categories.value.sort()
    localStorage.setItem('categories', JSON.stringify(categories.value))
    newItem.value.category = trimmed
  }
  closeCategoryModal()
}

onMounted(() => {
  loadItems()
  // Splash Screen für 1.8 Sekunden anzeigen
  setTimeout(() => {
    showSplash.value = false
  }, 1800)
})
</script>

<style>
/* Import modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Global styles - entfernt weißen Rand beim Scrollen */
html, body {
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  background-attachment: fixed;
  overflow-x: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: rgba(15, 12, 41, 0.5);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #764ba2, #667eea);
}

/* Firefox Scrollbar */
* {
  scrollbar-width: thin;
  scrollbar-color: #667eea rgba(15, 12, 41, 0.5);
}
</style>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.app-container {
  min-height: 100vh;
  background: transparent;
  position: relative;
  overflow-x: hidden;
}

/* Decorative Frame Overlay */
.frame-overlay {
  position: fixed;
  inset: 16px;
  border-radius: 24px;
  pointer-events: none;
  z-index: 10;
  box-shadow: 
    inset 0 0 80px rgba(102, 126, 234, 0.03),
    inset 0 0 40px rgba(118, 75, 162, 0.05),
    0 0 100px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.03);
}

/* Splash Screen */
.splash-screen {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(15, 12, 41, 0.98) 0%, rgba(48, 43, 99, 0.98) 50%, rgba(36, 36, 62, 0.98) 100%);
  backdrop-filter: blur(10px);
  z-index: 9999;
}

.splash-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: splashAnimation 1.5s cubic-bezier(0.4, 0, 0.2, 1), gradientShift 3s ease infinite;
  letter-spacing: -0.02em;
  text-align: center;
  filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
}

@keyframes splashAnimation {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.9);
  }
  60% {
    opacity: 1;
    transform: translateY(-10px) scale(1.05);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.content-hidden {
  opacity: 0;
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
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  border: 1px solid rgba(102, 126, 234, 0.4);
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(102, 126, 234, 0.3);
  border-color: rgba(102, 126, 234, 0.6);
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.9);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #ffffff;
  text-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
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

.glow-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23667eea' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  padding-right: 2.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glow-select:hover {
  background-color: rgba(255, 255, 255, 0.08);
  border-color: rgba(102, 126, 234, 0.5);
  transform: translateY(-1px);
}

.glow-select:focus {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23667eea' d='M6 3L1 8h10z'/%3E%3C/svg%3E");
  animation: selectPulse 0.3s ease;
}

@keyframes selectPulse {
  0% {
    box-shadow: 0 0 0 rgba(102, 126, 234, 0.3);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(102, 126, 234, 0);
  }
  100% {
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
  }
}

.glow-select option {
  background: #302b63;
  color: white;
  padding: 0.5rem;
  font-weight: 500;
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

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1rem;
}

.modal-content {
  background: linear-gradient(135deg, rgba(48, 43, 99, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: modalSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalSlideIn {
  0% {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modal-input {
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.modal-button {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.modal-button .icon {
  width: 18px;
  height: 18px;
}

.modal-button.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.modal-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.modal-button.secondary {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.modal-button.secondary:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: translateY(-20px) scale(0.95);
  opacity: 0;
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
