<template>
  <div class="about-section" id="about">
    <h2>Sobre nosotras</h2>
    <p>
      Somos Koral Tubía y Sonia Aoi García, dos estudiantes de tercer curso de Ciencia e Ingenieria de datos. 
    </p>
    <p>
      En este portfolio podrás encontrar los distintos proyectos que hemos ido haciendo a lo largo de nuestro trayecto en la carrera
    </p>
  </div>
</template>

<script>
export default {
  name: "AboutSection", 
};
</script>

<style scoped>
.about-section {
  position: relative;
  padding: 80px 20px; 
  margin-top: 50px; 
  background-color: rgba(0, 0, 0, 0.7); 
  color: white;
  border-radius: 10px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  z-index: 1; 
}


.about-section h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: white;
}

.about-section p {
  font-size: 18px;
  line-height: 1.6;
  color: white;
}

</style>
