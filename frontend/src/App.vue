<script setup>
// Imports:

import AboutSection from './components/AboutSection.vue'
import PageTitle from '@/components/PageTitle.vue'
import SearchSection from './components/SearchSection.vue'
import { ref, onMounted } from 'vue'
import axios from './plugins/axios'; 

// Estados:

//autenticación
const isAuthenticated = ref(false)
const authToken = ref('')
const username = ref('')
const password = ref('')
const message = ref('')

// proyectos
const projects = ref([])
const newProject = ref({
  titulo: '',
  autor: '',
  fecha: '',
  descripcion: '',
  imagen_url: ''
})

// Métodos:

//para iniciar sesión
const login = async () => {
  try {
    const response = await axios.post('/api/login', {
      username: username.value,
      password: password.value
    })
    
    authToken.value = response.data.access_token

    axios.defaults.headers.common['Authorization'] = `Bearer ${authToken.value}`
    
    isAuthenticated.value = true
    message.value = "Inicio de sesión exitoso."
    
    username.value = ''
    password.value = ''
    
    await fetchProjects()  
  } catch (error) {
    console.error("Error al iniciar sesión:", error)
    message.value = "Error: Credenciales incorrectas."
  }
}

// agregar o actualizar
const editingProjectId = ref(null)  

const addOrUpdateProject = async () => {
  try {
    const url = editingProjectId.value
      ? `/api/proyectos/${editingProjectId.value}`
      : '/api/proyectos'

    const method = editingProjectId.value ? 'put' : 'post'
    const response = await axios[method](url, newProject.value)

    message.value = response.data.msg
    await fetchProjects()

    if (response.status === 200 || response.status === 201) {
      newProject.value = { titulo: '', autor: '', fecha: '', descripcion: '', imagen_url: '' }
      editingProjectId.value = null
    }
  } catch (error) {
    console.error("Error al guardar el proyecto:", error)
    message.value = error.response?.data?.msg || "Error: No tienes permiso para añadir o editar proyectos."
  }
}

// cargar datos del proyecto en el formulario para editar
const editProject = (project) => {
  editingProjectId.value = project.id 
  newProject.value = { ...project }  
  scrollToSection('project-form')
}


// cerrar sesión
const logout = () => {
  isAuthenticated.value = false
  authToken.value = ''

  delete axios.defaults.headers.common['Authorization']

  newProject.value = {
    titulo: '',
    autor: '',
    fecha: '',
    descripcion: '',
    imagen_url: ''
  }
  
  editingProjectId.value = null
  
  message.value = ''
}

// proyectos
const fetchProjects = async () => {
  try {
    const headers = authToken.value 
      ? { Authorization: `Bearer ${authToken.value}` }
      : {}
    
    const response = await axios.get('/api/proyectos', { headers })
    projects.value = response.data
  } catch (error) {
    console.error("Error al obtener proyectos:", error)
  }
}

//eliminar proyectos
const deleteProject = async (id) => {
  try {
    const response = await axios.delete(`/api/proyectos/${id}`, 
      { headers: { Authorization: `Bearer ${authToken.value}` } }
    )
    message.value = response.data.message
    await fetchProjects()
  } catch (error) {
    console.error("Error al eliminar el proyecto:", error)
    message.value = "Error: No tienes permiso para eliminar proyectos."
  }
}

// desplazarse a una sección
const scrollToSection = (sectionId) => {
  const section = document.getElementById(sectionId)
  if (section) {
    const offset = 70
    const topPosition = section.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({
      top: topPosition,
      behavior: 'smooth'
    })
  }
}

//manejar error de imagen
const handleImageError = (project) => {
  console.error(`Error al cargar la imagen para el proyecto: ${project.titulo}`);
  project.imagen_url = null; 
}

//se cargan siempre los proyectos
onMounted(() => {
  fetchProjects()  
})

</script>



<template>
  <div class="app-container">
    <nav class="navbar">
      <div class="nav-content">
        <div class="nav-brand">
          <PageTitle msg="Portfolio" class="nav-title" />
        </div>
        <ul class="nav-links">
          <li><a href="#buscador" @click.prevent="scrollToSection('buscador')">Buscador</a></li>
          <li><a href="#proyectos" @click.prevent="scrollToSection('proyectos')">Proyectos</a></li>
          <li><a href="#about" @click.prevent="scrollToSection('about')">Sobre Nosotras</a></li>
          <li v-if="isAuthenticated"><button @click="logout">Cerrar Sesión</button></li>
        </ul>
      </div>
    </nav>

    <main class="content-wrapper">
      <section id="buscador" class="sectionBuscador">
        <SearchSection :projects="projects" />
      </section>

      <!-- Sección de inicio de sesión -->
      <section id="login" v-if="!isAuthenticated">
        <h2>Iniciar Sesión para gestionar proyectos</h2>
        <form @submit.prevent="login">
          <label>Usuario:</label>
          <input type="text" v-model="username" required />

          <label>Contraseña:</label>
          <input type="password" v-model="password" required />

          <button type="submit">Iniciar Sesión</button>
        </form>
        <p v-if="message">{{ message }}</p>
      </section>

      <!-- Sección de proyectos -->
      <section id="proyectos" class="sectionProyectos">
        <h1>Proyectos</h1>

        <!-- Formulario para agregar o actualizar un proyecto -->
        <template v-if="isAuthenticated">
          <h2>{{ editingProjectId ? 'Actualizar Proyecto' : 'Agregar Proyecto' }}</h2>
          <form @submit.prevent="addOrUpdateProject" class="project-form" id="project-form">
            <div class="form-group">
              <label>Título:</label>
              <input type="text" v-model="newProject.titulo" required />
            </div>

            <div class="form-group">
              <label>Autor:</label>
              <input type="text" v-model="newProject.autor" required />
            </div>

            <div class="form-group">
              <label>Fecha:</label>
              <input type="date" v-model="newProject.fecha" />
            </div>

            <div class="form-group">
              <label>Descripción:</label>
              <textarea v-model="newProject.descripcion"></textarea>
            </div>

            <div class="form-group">
              <label>URL de la imagen:</label>
              <input 
                type="text" 
                v-model="newProject.imagen_url" 
                placeholder="Introduce la URL de la imagen"
                class="image-input"
              />
            </div>

            <div v-if="newProject.imagen_url" class="image-preview">
              <img 
                :src="newProject.imagen_url" 
                alt="Vista previa"
                @error="handleImageError"
              />
            </div>

            <button type="submit" class="submit-button">
              {{ editingProjectId ? 'Actualizar Proyecto' : 'Guardar Proyecto' }}
            </button>
          </form>
        </template>

        <!-- Lista de proyectos -->
        <h2>---------------</h2>
        <ul>
          <li
            v-for="project in projects"
            :key="project.id"
            :id="`project-${project.id}`"
            class="project-card"
          >
            <div class="project-content">
              <h3>{{ project.titulo }}</h3>
              <p><strong>Autor:</strong> {{ project.autor }}</p>
              <p><strong>Fecha:</strong> {{ project.fecha }}</p>
              <p><strong>Descripción:</strong> {{ project.descripcion }}</p>
              <div class="project-image-container">
                <img 
                  v-if="project.imagen_url"
                  :src="project.imagen_url" 
                  :alt="project.titulo"
                  class="project-image"
                  @error="handleImageError(project)"
                />
                <div v-else class="placeholder-image">
                  No hay imagen disponible
                </div>
              </div>
              
              <div v-if="isAuthenticated" class="admin-buttons">
                <button @click="editProject(project)">Editar</button>
                <button @click="deleteProject(project.id)">Eliminar</button>
              </div>
            </div>
          </li>
        </ul>

        <p v-if="message">{{ message }}</p>
      </section>

      <section id="about" class="sectionAbout">
        <AboutSection />
      </section>
    </main>
  </div>
</template>

<style>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: white;
  z-index: 1000;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: -30px ; 
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.logo {
  width: 50px; 
  height: 50px; 
  margin-right: 10px;
}

.nav-title {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.navbar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 40px; 
}

.navbar ul li {
  display: inline;
}

.navbar ul li a {
  color: #333;
  text-decoration: none;
  font-size: 20px; 
}

.navbar ul li a:hover {
  color: hsl(304, 100%, 50%);
}

.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
}

.search-results {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  overflow: hidden;
}

.search-result-item {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.search-result-item:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.no-results {
  color: white;
  text-align: center;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
}

.buscador-container {
  margin-top: auto; 
  padding: 70px 0;
  background-color: rgba(0, 0, 0, 0.5);
}

.buscador-container :deep(.buscador) {
  width: 80%;
  max-width: 600px;
  margin: 0 auto;
}

.login-container {
    position: relative;
    z-index: 2;
}

.about-container {
    position: relative;
    z-index: 1;
}

.sectionBuscador {
  display: flex;
  justify-content: center; 
  align-items: center; 
  padding: 0; 
  height: 100vh;
}

.sectionProyectos {
  padding: 400px 0;
}
.sectionAbout {
  padding: 100px 0;
}
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  background-image: url('@/assets/Gif.gif');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
  background-attachment: fixed;
  color: white; 
}

#app {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  color: white; 
}


input, textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  color: black; 
  background-color: white; 
}


button {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}


form {
  margin-bottom: 20px;
}

label {
  display: block;
  margin: 8px 0 4px;
  color: white; 
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background-color: rgba(0, 0, 0, 0.5); 
}

h1, h2 {
  color: white; 
}

.project-card {
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
}

.project-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.project-image-container {
  width: 100%;
  height: 400px;
  margin: 15px 0;
  border-radius: 8px;
  overflow: hidden;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.project-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-style: italic;
  background-color: rgba(255, 255, 255, 0.1);
}

input[type="text"], 
input[type="date"], 
textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background-color: white;
  color: black;
}
</style>
