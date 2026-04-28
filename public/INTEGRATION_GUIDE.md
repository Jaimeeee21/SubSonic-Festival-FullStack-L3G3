/**
 * GUÍA: INTEGRACIÓN FRONTEND - BACKEND
 * SubSonic Festival
 * 
 * Esta guía muestra cómo adaptar los archivos *-data.js para que funcionen
 * tanto con mock data como con el backend, simplemente cambiando:
 * 
 * CONFIG.USE_BACKEND = false  -> Usa JSON mock (estado actual)
 * CONFIG.USE_BACKEND = true   -> Usa API backend
 */

// ============================================================================
// PASO 1: Asegurar que config.js esté cargado ANTES de otros scripts
// ============================================================================

// En index.html, asegurarse de que el orden es:
// 1. <script src="view/config.js"></script>      ⬅️ PRIMERO
// 2. <script src="view/script.js"></script>
// 3. <script src="view/{pagina}-data.js"></script>
// 4. <script src="view/{pagina}-view.js"></script>


// ============================================================================
// PASO 2: Patrón de adaptación para archivos *-data.js
// ============================================================================

/**
 * ANTES (estado actual - solo mock):
 * 
 * window.EVENTOS_DATA = {
 *   "principales": [ ... ]
 * }
 * 
 * 
 * DESPUÉS (frontend/backend flexible):
 */

// EJEMPLO ADAPTADO - eventos-data.js
(function initEventosData() {
    // Si estamos usando backend, cargar desde API
    if (CONFIG.USE_BACKEND) {
        // Cargar eventos del backend
        fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventos)
            .then(response => response.json())
            .then(data => {
                // Transformar respuesta backend al formato que espera el frontend
                window.EVENTOS_DATA = transformEventosFromBackend(data);
                // Disparar evento para que las vistas se actualicen
                window.dispatchEvent(new Event('datosActualizados'));
            })
            .catch(error => {
                console.error('Error cargando eventos del backend:', error);
                console.warn('Usando mock data como fallback');
                // Cargar desde JSON mock como fallback
                loadMockEventos();
            });
    } else {
        // Cargar mock data desde JSON
        loadMockEventos();
    }
})();

function loadMockEventos() {
    fetch('eventos-data.json?t=' + Date.now())
        .then(response => response.json())
        .then(data => {
            window.EVENTOS_DATA = data;
            window.dispatchEvent(new Event('datosActualizados'));
        })
        .catch(error => console.error('Error cargando eventos:', error));
}

/**
 * Transformar respuesta del backend al formato frontend
 * 
 * El backend devuelve un array de objetos EventoResponse
 * Necesitamos agruparlos bajo "principales" como espera el frontend
 */
function transformEventosFromBackend(eventosArray) {
    return {
        principales: eventosArray.map(evento => ({
            id: evento.id,
            title: evento.titulo,
            date: evento.fecha,
            location: evento.ubicacion,
            description: evento.descripcion,
            image: evento.imagen_url,
            info: evento.info || [],
            artists: evento.artistas || {}
        }))
    };
}


// ============================================================================
// PASO 3: Aplicar el mismo patrón a otros archivos
// ============================================================================

/**
 * ARCHIVOS A ADAPTAR:
 * 
 * ✅ eventos-data.js         -> API: /api/eventos
 * ✅ productos-data.js       -> API: /api/productos
 * ✅ usuarios-data.js        -> API: /api/usuarios (login/registro)
 * ✅ reservas-data.js        -> API: /api/reservas
 * ✅ espacios-data.js        -> API: /api/espacios
 * 
 * Cada uno siguiendo el mismo patrón:
 * 1. Verificar CONFIG.USE_BACKEND
 * 2. Si true: fetch desde API
 * 3. Si false: fetch desde JSON mock
 * 4. Transformar datos si es necesario
 */


// ============================================================================
// PASO 4: Adaptar las vistas (*-view.js)
// ============================================================================

/**
 * Los archivos *-view.js no necesitan cambios importantes porque
 * solo leen window.EVENTOS_DATA, window.PRODUCTOS_DATA, etc.
 * 
 * El cambio automático se produce en los archivos *-data.js
 * 
 * PERO: Si necesitas hacer peticiones adicionales (guardar datos, etc),
 * usa la función fetchAPI() de config.js
 * 
 * EJEMPLO - Crear una reserva:
 */

async function crearReservaDesdeVista(datosReserva) {
    if (CONFIG.USE_BACKEND) {
        try {
            const response = await fetchAPI(CONFIG.ENDPOINTS.reservas, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datosReserva)
            });
            return response;
        } catch (error) {
            console.error('Error creando reserva:', error);
            return null;
        }
    } else {
        // Con mock: solo guardar en localStorage o mostrar confirmación local
        console.log('Mock: Reserva guardada localmente', datosReserva);
        // Aquí irían acciones con mock data (localStorage, etc)
        return { id: Math.random(), ...datosReserva };
    }
}


// ============================================================================
// PASO 5: Variables a reemplazar en cada archivo
// ============================================================================

/**
 * EVENTOS-DATA.JS
 * ----------------
 * Buscar: window.EVENTOS_DATA = {
 * Reemplazar el contenido completo con la función initEventosData()
 * 
 * 
 * PRODUCTOS-DATA.JS
 * -----------------
 * window.PRODUCTOS_DATA = { "categories": [...] }
 * 
 * Adaptación:
 * if (CONFIG.USE_BACKEND) {
 *     fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.productos)
 *         .then(response => response.json())
 *         .then(data => {
 *             window.PRODUCTOS_DATA = transformProductosFromBackend(data);
 *             // datos en formato: { categories: [...] }
 *         })
 * }
 * 
 * 
 * USUARIOS-DATA.JS (login/registro)
 * ----------------------------------
 * Usar fetchAPI para POST/login y POST/registro
 * 
 * 
 * RESERVAS-DATA.JS
 * ----------------
 * GET: /api/reservas + /api/reservas/usuario/{id}
 * POST: /api/reservas (crear)
 * PUT: /api/reservas/{id}/confirmar (confirmar)
 * 
 * 
 * ESPACIOS-DATA.JS (reservas de espacios)
 * ----------------------------------------
 * GET: /api/espacios + /api/espacios/disponibles/all
 * POST: /api/espacios (crear)
 */


// ============================================================================
// PASO 6: Checklist de implementación
// ============================================================================

/*
CHECKLIST:
□ config.js ya está listo (archivo creado)
□ Adaptar eventos-data.js
□ Adaptar productos-data.js
□ Adaptar usuarios-data.js (login/registro)
□ Adaptar reservas-data.js
□ Adaptar espacios-data.js
□ Verificar orden de scripts en HTML
□ Pruebas con CONFIG.USE_BACKEND = false (mock)
□ Pruebas con CONFIG.USE_BACKEND = true (backend)
□ Manejar errores de conexión
□ Implementar retry logic si es necesario

PRÓXIMAS MEJORAS (opcionales):
□ Implementar autenticación JWT
□ Almacenar token en localStorage
□ Actualizar headers en fetchAPI para incluir token
□ Implementar invalidación de cache
□ Agregar estado de carga (spinners, etc)
*/


// ============================================================================
// PASO 7: Testing - Verificar integración
// ============================================================================

/**
 * Abrir la consola del navegador (F12) y ejecutar:
 * 
 * // Ver modo actual
 * console.log(CONFIG);
 * 
 * // Simular cambio a backend
 * CONFIG.USE_BACKEND = true;
 * 
 * // Hacer un test de fetch
 * fetchAPI(CONFIG.ENDPOINTS.eventos)
 *     .then(data => console.log('✅ Backend disponible:', data))
 *     .catch(err => console.error('❌ Error:', err));
 */

console.log('%c📖 GUÍA: Abre este archivo para ver cómo integrar frontend con backend', 
    'color: #00d4ff; font-size: 12px; font-weight: bold;');
