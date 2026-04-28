# 🔄 Cambiar entre Mock Data y Backend Real

## ¿Cómo funciona?

El proyecto tiene un sistema de **toggle** que permite elegir si usar:
- **Mock Data** (datos locales en archivos JSON) - Para desarrollo rápido
- **Backend Real** (datos desde Firestore) - Para testing final

## ¿Dónde cambiar?

### 📁 Archivo: `config.js` (línea ~12)

```javascript
const CONFIG = {
    // ============ CAMBIAR AQUÍ ============
    USE_BACKEND: true,  // true = Backend real | false = Mock local
    // =====================================
```

## Opciones

### ✅ USE_BACKEND: `true` (RECOMENDADO - Backend Real)
```javascript
USE_BACKEND: true
```
- **Frontend carga datos desde**: `http://localhost:8000/api`
- **Backend debe estar corriendo**: `python run.py`
- **Ventajas**: 
  - Datos en tiempo real desde Firestore
  - Cambios en la BD se ven inmediatamente
  - Simula aplicación en producción
- **Desventajas**: 
  - Requiere que el backend esté ejecutando

### 📦 USE_BACKEND: `false` (Mock Data Local)
```javascript
USE_BACKEND: false
```
- **Frontend carga datos desde**: Archivos `-data.json` locales
- **Backend no es necesario**: El proyecto funciona sin servidor
- **Ventajas**: 
  - Desarrollo rápido sin backend
  - Sin dependencias externas
  - Funciona offline
- **Desventajas**: 
  - Datos estáticos
  - No refleja cambios en BD

## 📋 Archivos que usan el sistema

### Eventos
- `eventos-view.js` - Lee datos reales del backend o mock
- `eventos-data.js` - Contiene mock data (cuando `USE_BACKEND: false`)
- API Backend: `GET /api/eventos`

### Productos
- `product-detail-view.js` - Lee datos reales del backend o mock
- `product-detail-data.json` - Contiene mock data (cuando `USE_BACKEND: false`)
- API Backend: `GET /api/productos`

### Otros módulos
Mismo patrón para:
- Usuarios (`login-view.js`)
- Reservas (`reserva-view.js`)
- Espacios (`reserve-space-view.js`)

## 🚀 Instrucciones paso a paso

### Opción A: Usar Backend Real ⚡

1. **Asegúrate que Firebase esté configurado**
   - ✅ Ya lo está: `subsonic-festival-12f95`
   - ✅ Archivo de credenciales: `subsonic-festival-12f95-firebase-adminsdk-fbsvc-cce9bc18ef.json`

2. **Inicia el backend**
   ```bash
   cd SubSonic-Festival
   python run.py
   ```
   - Deberías ver: `INFO: Uvicorn running on http://0.0.0.0:8000`
   - El backend está listo cuando ves: `✅ Firebase inicializado correctamente`

3. **Abre `config.js` y cambia**
   ```javascript
   USE_BACKEND: true  // ← CAMBIAR A ESTO
   ```

4. **Recarga la página en el navegador**
   - F5 o Ctrl+R

5. **Abre la consola (F12) y verifica**
   - Deberías ver: `✅ Eventos cargados desde backend: ...`

### Opción B: Usar Mock Data Local 📦

1. **Abre `config.js` y cambia**
   ```javascript
   USE_BACKEND: false  // ← CAMBIAR A ESTO
   ```

2. **Recarga la página en el navegador**
   - F5 o Ctrl+R

3. **El backend NO es necesario**
   - Abre la consola (F12)
   - Deberías ver: `📦 Usando EVENTOS_DATA definido globalmente`

## 🛠️ Solución de problemas

### El frontend dice "Error cargando desde backend"

**Posibles causas:**
1. El backend no está corriendo
   - ✅ Solución: `python run.py`

2. El backend está en otro puerto
   - ✅ Solución: Edita `CONFIG.API_BASE_URL` en `config.js`

3. Hay CORS bloqueado
   - ✅ Solución: El backend ya tiene CORS habilitado

### Los datos no se actualizan aunque cambié en Firestore

1. Limpia la caché del navegador (Ctrl+Shift+Delete)
2. Recarga la página (Ctrl+R)
3. Verifica en Firestore Console que los datos están realmente actualizados

### ¿Cómo sé cuál modo está activo?

Abre la **consola del navegador (F12**):

```
⚙️ SubSonic Festival Configuration
Modo: 🔌 BACKEND    ← Backend activo
API Base URL: http://localhost:8000/api
```

o

```
⚙️ SubSonic Festival Configuration
Modo: 📦 MOCK DATA    ← Mock data activo
```

## 📝 Resumen Técnico

| Aspecto | Mock Data | Backend Real |
|---------|-----------|--------------|
| **Fuente** | Archivos JSON locales | API/Firestore |
| **USE_BACKEND** | `false` | `true` |
| **Backend requerido** | ❌ No | ✅ Sí |
| **Datos tiempo real** | ❌ No | ✅ Sí |
| **Velocidad** | ⚡ Muy rápido | 🐢 Depende de conexión |
| **Caso de uso** | Desarrollo inicial | Testing final, producción |

