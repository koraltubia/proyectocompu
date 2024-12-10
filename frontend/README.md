
---

# Portfolio de Proyectos

Este proyecto es una aplicación web que permite a los usuarios gestionar proyectos de un portafolio, con funcionalidades para realizar búsquedas, así como para crear, editar y eliminar proyectos. La aplicación cuenta con un sistema de autenticación para restringir ciertas acciones solo a usuarios registrados.

## Índice

1. [Descripción General](#descripción-general)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Ejecución del Proyecto](#ejecución-del-proyecto)
6. [Uso de Axios](#uso-de-axios)
7. [Explicación del Código](#explicación-del-código)
8. [Notas y Consideraciones](#notas-y-consideraciones)

---

### Descripción General

La aplicación permite a los usuarios autenticados gestionar proyectos en un portafolio. Los usuarios pueden iniciar sesión, crear nuevos proyectos, actualizarlos y eliminarlos según sea necesario. También existe una funcionalidad de búsqueda que permite a los usuarios buscar proyectos por título en tiempo real.

---

### Funcionalidades

- **Autenticación de Usuario**: Los usuarios deben iniciar sesión para acceder a las funciones de gestión de proyectos.
- **Gestión de Proyectos**: Creación, edición y eliminación de proyectos.
- **Buscador de Proyectos**: Permite buscar proyectos por título.
- **Vista de Detalles**: Cada proyecto cuenta con detalles específicos como título, autor, fecha, descripción e imagen.

---

### Tecnologías Utilizadas

- **Frontend**: Vue 3, HTML5, CSS3
- **Backend**: Flask para la API REST
- **Autenticación**: JWT (JSON Web Tokens) para el acceso a funcionalidades protegidas
- **HTTP Requests**: Axios para comunicación con la API

---

### Estructura del Proyecto

```plaintext
📁 proyecto
├── 📁 src
│   ├── App.vue
│   ├── main.js
│   ├── 📁 components
│   │   ├── AboutSection.vue
│   │   ├── PageTitle.vue
│   │   ├── SearchSection.vue
│   ├── 📁 plugins
│   │   ├── axios.js
│   └── 📁 assets
│       └── Gif.gif

├── 📁 backend
│   ├── backend.py
│   └── 📁 instance
│       └── projects.db
└── README.md
```

---

### Ejecución del Proyecto

#### Backend (Flask)

1. **Instalar Dependencias**:
   ```
   pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Flask-CORS werkzeug
   ```

2. **Iniciar el Servidor**:
   ```
   python backend/backend.py
   ```
   
#### Frontend (Vue)

1. **Navegar a la Carpeta `src`**:
   ```
   cd src
   ```

2. **Instalar Dependencias**:
   ```
   npm install
   ```

3. **Ejecutar el Servidor de Desarrollo**:
   ```
   npm run serve
   ```
   
---

### Uso de Axios

**Axios** es una biblioteca de cliente HTTP basada en promesas que permite realizar solicitudes a la API REST del backend. A continuación se describen algunas de las operaciones principales realizadas con Axios en el proyecto:

- **Autenticación**:
  - Al iniciar sesión, se realiza una solicitud `POST` a `/api/login` con las credenciales del usuario. Si la autenticación es exitosa, se recibe un token JWT que se almacena en el almacenamiento local del navegador para su uso en futuras solicitudes.
  
- **Gestión de Proyectos**:
  - Para crear un nuevo proyecto, se realiza una solicitud `POST` a `/api/proyectos`, enviando los datos del proyecto. Para editar y eliminar, se utilizan las solicitudes `PUT` y `DELETE`, respectivamente, pasando el ID del proyecto.

- **Búsqueda de Proyectos**:
  - Durante la búsqueda de proyectos, se puede utilizar una solicitud `GET` a `/api/proyectos` para obtener la lista de todos los proyectos y luego filtrar los resultados en el frontend.
---

### Explicación del Código

#### `App.vue`

Componente principal que organiza la aplicación, incluye:
- **Barra de navegación**: Permite acceder a las distintas secciones.
- **Gestión de proyectos**: Con autenticación, permite crear, editar y eliminar proyectos.
- **Navegación entre secciones**: Proporciona una estructura intuitiva para moverse dentro de la aplicación.

#### `SearchSection.vue`

Este componente es responsable de la búsqueda de proyectos, con:
- **Campo de búsqueda**: Filtra proyectos por título.
- **Visualización de resultados**: Muestra los proyectos que coinciden con el término ingresado.

#### `PageTitle.vue`

Un componente llamativo para mostrar el título de cada página o sección, personalizado con efectos visuales atractivos.

#### `AboutSection.vue`

Este componente ofrece información sobre las creadoras del portafolio y la finalidad del proyecto.

---

### Backend (`backend.py`)

El backend implementa la API REST para manejar usuarios y proyectos.

#### Funcionalidades principales

- **Autenticación de Usuarios**:
  - `POST /api/login`: Verifica las credenciales del usuario y devuelve un token JWT.
  
- **Operaciones CRUD para Proyectos**:
  - `POST /api/proyectos`: Crea un nuevo proyecto.
  - `GET /api/proyectos`: Obtiene todos los proyectos.
  - `DELETE /api/proyectos/<int:id>`: Elimina un proyecto (requiere autenticación y validación de usuario).
  - `PUT /api/proyectos/<int:id>`: Edita los detalles de un proyecto (requiere autenticación y validación de usuario).

#### Configuración e Inicialización de la Base de Datos

- Al iniciar el servidor, se crea la base de datos `projects.db` automáticamente en la carpeta `instance/` si no existe, junto con dos usuarios de prueba (`admin` y `user`, cuyas contraseñas son `adminpass` y  `userpass` respectivamente).
---

### Notas y Consideraciones

- **Manejo de Errores**: Se manejan errores en autenticación y permisos al gestionar proyectos.
- **Autenticación JWT**: Se requiere autenticación para manejar proyectos; las solicitudes están protegidas mediante tokens JWT.
- **Validación de Campos**: El frontend valida los campos antes de enviar datos al backend, reduciendo errores de entrada.
- **Edición de Proyectos en Formulario**: Al editar un proyecto, los datos actuales del proyecto se rellenan automáticamente en el formulario, lo que permite al usuario ver y realizar cambios específicos en el mismo. Después de ajustar los datos, el usuario debe actualizar el proyecto desde el formulario.

--- 