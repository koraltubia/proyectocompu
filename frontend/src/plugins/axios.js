
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: https://proyectocompu-duwp.onrender.com,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

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
