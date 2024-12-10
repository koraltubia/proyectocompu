<template>
  <div class="buscador">
    <input
      v-model="searchTerm"
      @input="search"
      type="text"
      placeholder="Buscar proyectos..."
      class="search-input"
    />
    <ul v-if="searchResults.length > 0" class="search-results">
      <li 
        v-for="project in searchResults" 
        :key="project.id" 
        class="search-result-item"
        @click="selectProject(project.id)"
      >
        <h3>{{ project.titulo }}</h3>
        <p>{{ project.descripcion }}</p>
      </li>
    </ul>
    <p v-else-if="searchTerm && searchResults.length === 0" class="no-results">
      No se encontraron resultados.
    </p>
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'SearchSection',
  props: {
    projects: {
      type: Array,
      required: true
    }
  },
  setup(props) {

  // Métodos:

  //búsqueda

  const searchTerm = ref('');
  const searchResults = ref([]);

  const search = () => {
  if (!searchTerm.value) { 
    searchResults.value = [];
    return;
  }


  searchResults.value = props.projects.filter(project => 
    project.titulo.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    project.descripcion?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    project.autor?.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
};

  const selectProject = (projectId) => {
    console.log('Seleccionando proyecto:', projectId);
    
    const proyectosSection = document.getElementById('proyectos');
    if (proyectosSection) {
      proyectosSection.scrollIntoView({ behavior: 'smooth' });
    }

    setTimeout(() => {
      const projectElement = document.getElementById(`project-${projectId}`);
      if (projectElement) {

        projectElement.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'center' 
        });
        

        projectElement.classList.add('highlight');
        setTimeout(() => {
          projectElement.classList.remove('highlight');
        }, 2000);
      }
    }, 500);


    searchTerm.value = '';
    searchResults.value = [];
  };


  watch(() => props.projects, () => {
    if (searchTerm.value) {
      search();
    }
  });

  return {
    searchTerm,
    searchResults,
    search,
    selectProject
  };
}
}
</script>
<style scoped>
.buscador {
  margin-bottom: 20px;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
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
  list-style-type: none;
  padding: 0;
  margin-top: 10px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  overflow: hidden;
}

.search-result-item {
  padding: 15px;
  cursor: pointer;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.search-result-item:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.search-result-item h3 {
  margin-top: 0;
  color: #333;
}

.search-result-item p {
  color: #666;
  margin: 5px 0 0;
}

.no-results {
  color: white;
  text-align: center;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
}

:deep(.highlight) {
  animation: highlight 2s ease-out;
}

@keyframes highlight {
  0% {
    background-color: rgba(255, 215, 0, 0.3);
    transform: scale(1.02);
  }
  50% {
    background-color: rgba(255, 215, 0, 0.5);
    transform: scale(1.02);
  }
  100% {
    background-color: rgba(0, 0, 0, 0.5);
    transform: scale(1);
  }
}
</style>