<template>
    <h1 class="nav-title">{{ msg }}</h1>
</template>
  
<script setup>
import { defineProps } from 'vue'  

defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.nav-title {
  margin: 0;
  font-family: 'Pacifico', cursive; 
  font-size: 38px;
  font-weight: bold;
  color: #333333; 
  background: linear-gradient(90deg, #ff8a00, #ff0080, #0072ff); 
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;

  text-shadow: 0 0 3px rgba(255, 255, 255, 0.3), 
              0 0 5px rgba(255, 140, 0, 0.4),
              0 0 8px rgba(255, 0, 128, 0.5),
              0 0 10px rgba(0, 114, 255, 0.6);

  transition: text-shadow 0.3s ease-in-out;
}

.nav-title:hover {
  text-shadow: 0 0 6px rgba(255, 255, 255, 0.5),
              0 0 10px rgba(255, 140, 0, 0.7),
              0 0 15px rgba(255, 0, 128, 0.8),
              0 0 20px rgba(0, 114, 255, 0.9);
}
</style>