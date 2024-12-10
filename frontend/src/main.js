import { createApp } from 'vue';
import App from './App.vue';
import axios from './plugins/axios'; // Importamos axios

const app = createApp(App);


app.config.globalProperties.$axios = axios;

app.mount('#app');

