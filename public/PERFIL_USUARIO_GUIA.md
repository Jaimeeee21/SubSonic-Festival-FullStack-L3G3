# Guía de Uso - Sistema de Perfil de Usuario

## Introducción
Se ha implementado un sistema completo de perfil de usuario en SubSonic Festival que permite a los usuarios gestionar su información personal, foto de perfil y ver todas las entradas que han comprado.

## Archivos Principales Creados/Modificados

### Backend
- **app/DTOs/usuario_dto.py** - DTOs actualizados con nuevos campos
- **app/dao/usuario_dao.py** - Nuevos métodos para foto de perfil
- **app/services/usuario_service.py** - Nuevos servicios para perfil
- **app/routes/usuarios.py** - Nuevos endpoints

### Frontend
- **public/profile.html** - Página de perfil
- **public/profile-data.js** - Gestión de datos
- **public/profile-view.js** - Lógica de interfaz
- **public/style.css** - Estilos actualizados

## Cómo Acceder

1. El usuario debe iniciar sesión primero
2. Acceder a la URL: `http://localhost:PORT/profile.html`
3. La página cargará automáticamente los datos del usuario desde la base de datos

## Funcionalidades

### 1. Ver Información del Perfil
- Nombre completo
- Email
- Teléfono
- Ciudad
- Fecha de registro
- Tipo de usuario (Individual/Empresa)
- Biografía

### 2. Cambiar Foto de Perfil
1. Hacer clic en el botón de cámara sobre la foto actual
2. Seleccionar una imagen (formatos: JPG, PNG, GIF, WEBP)
3. La foto se sube automáticamente en base64
4. Se actualiza en tiempo real en la BD

### 3. Editar Información
1. Hacer clic en el botón "Editar Perfil"
2. Se abrirá un modal con todos los campos editables
3. Modificar los datos deseados
4. Hacer clic en "Guardar Cambios"
5. Los datos se actualizan en la BD

### 4. Ver Entradas Compradas
- Se muestran todas las reservas del usuario en un grid
- Cada tarjeta muestra:
  - Nombre del evento
  - Estado (Confirmada/Pendiente/Cancelada)
  - Fecha del evento
  - Cantidad de entradas
  - Precio total
  - ID de referencia
- Botones para:
  - **Descargar**: Obtener la entrada (PDF/Documento)
  - **Detalles**: Ver más información

### 5. Logout
- Botón "Cerrar Sesión" en la esquina superior derecha
- Limpia la sesión y redirige a login.html

## Estructura de API

### Endpoints Nuevos

**GET /api/usuarios/{usuario_id}/perfil**
- Obtiene perfil completo del usuario con sus entradas
- Respuesta:
```json
{
  "usuario": { ... datos usuario ... },
  "entradas": [ { ... reservas ... } ]
}
```

**PUT /api/usuarios/{usuario_id}/foto-perfil**
- Actualiza la foto de perfil
- Body:
```json
{
  "foto_perfil": "base64_data_url"
}
```

**PUT /api/usuarios/{usuario_id}**
- Actualiza información del perfil
- Body:
```json
{
  "nombre": "Nuevo nombre",
  "email": "nuevo@email.com",
  "telefono": "+34...",
  "ciudad": "Madrid",
  "bio": "Mi biografía"
}
```

## Almacenamiento de Datos

La información se almacena en Firestore bajo la colección `usuarios`:

```
usuarios/
├── user_id_1/
│   ├── nombre: "Juan García"
│   ├── email: "juan@example.com"
│   ├── foto_perfil: "data:image/jpeg;base64,..."
│   ├── telefono: "+34912345678"
│   ├── ciudad: "Madrid"
│   ├── bio: "Aficionado a la música"
│   ├── es_empresa: false
│   └── created_at: "2024-01-01T10:30:00"
└── ...
```

## Validaciones

- **Email**: Debe ser único, debe tener formato de email válido
- **Foto**: Máximo 5MB, solo formatos de imagen
- **Teléfono**: Campo opcional, texto libre
- **Bio**: Campo opcional, máximo 500 caracteres

## Notas Importantes

1. **Autenticación**: La página redirige automáticamente a login.html si no hay usuario autenticado
2. **Foto de Perfil**: Se almacena en base64 en la BD. Para usar URLs externas, modificar `profile-data.js`
3. **Entradas**: Requiere que exista el endpoint `/api/reservas/usuario/{id}`
4. **Seguridad**: La contraseña NO se puede cambiar desde el perfil (se debe usar página separada)

## Troubleshooting

### Problema: "La página redirige a login"
**Solución**: Asegúrate de que has iniciado sesión correctamente y que el ID está guardado en localStorage

### Problema: "No se carga la foto"
**Solución**: Verifica que la imagen sea menor a 5MB y en formato válido

### Problema: "No se ve ninguna entrada"
**Solución**: Asegúrate de que el usuario tiene reservas y que el endpoint de reservas existe

### Problema: "Error al actualizar perfil"
**Solución**: Verifica la consola del navegador para ver el error específico de la API

## Ejemplos de Uso

### Con cURL

**Obtener perfil:**
```bash
curl -X GET http://localhost:8000/api/usuarios/user123/perfil
```

**Actualizar foto:**
```bash
curl -X PUT http://localhost:8000/api/usuarios/user123/foto-perfil \
  -H "Content-Type: application/json" \
  -d '{"foto_perfil":"data:image/jpeg;base64,..."}'
```

**Editar información:**
```bash
curl -X PUT http://localhost:8000/api/usuarios/user123 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Nuevo Nombre","ciudad":"Barcelona"}'
```

## Personalización

### Cambiar URL de API
Modificar en `public/config.js`:
```javascript
window.API_BASE_URL = 'http://tu-servidor:puerto/api';
```

### Cambiar estilos
Los estilos están en `public/style.css` bajo la sección "PERFIL DEL USUARIO"

### Cambiar textos
Los textos están principalmente en `profile.html` y pueden ser personalizados

## Soporte
Para reportar problemas o sugerencias, contacta al equipo de desarrollo.
