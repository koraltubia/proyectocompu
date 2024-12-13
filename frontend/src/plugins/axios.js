
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: "https://proyectocompu-duwp.onrender.com", // La URL debe estar entre comillas
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export default axiosInstance;

axiosInstance.interceptors.request.use(request => {
  console.log('Starting Request:', request)
  return request
})

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    console.error('Error en la petición:', error.response);
    if (error.response.status === 401) {
      console.log('Error de autenticación');
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
