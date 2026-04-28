/**
 * CONFIGURACIÓN GLOBAL DE SUBSONIC FESTIVAL
 * 
 * Cambiar 'USE_BACKEND' a true/false para intercambiar entre backend real y mock data
 * 
 * true  = Usar API del backend (http://localhost:8000)
 * false = Usar JSON mock local (compatible con versión actual)
 */

const CONFIG = {
    // ============ CAMBIAR AQUÍ ============
    USE_BACKEND: true,  // true = Backend real | false = Mock local
    // =====================================
    
    API_BASE_URL: "http://localhost:8000/api",
    
    // Timeouts y reintentos
    FETCH_TIMEOUT: 5000,
    MAX_RETRIES: 3,
    
    // Endpoints disponibles
    ENDPOINTS: {
        // Usuarios
        usuarios: "/usuarios",
        login: "/usuarios/login",
        registro: "/usuarios/registro",
        
        // Eventos
        eventos: "/eventos",
        eventosPorUbicacion: (ubicacion) => `/eventos/ubicacion/${ubicacion}`,
        
        // Productos
        productos: "/productos",
        productosPorCategoria: (categoria) => `/productos/categoria/${categoria}`,
        
        // Reservas
        reservas: "/reservas",
        reservasUsuario: (usuarioId) => `/reservas/usuario/${usuarioId}`,
        reservasEvento: (eventoId) => `/reservas/evento/${eventoId}`,
        
        // Espacios
        espacios: "/espacios",
        espaciosPorTipo: (tipo) => `/espacios/tipo/${tipo}`,
        espaciosDisponibles: "/espacios/disponibles/all",
        espaciosUsuario: (usuarioId) => `/espacios/usuario/${usuarioId}`
    }
};

/**
 * Función auxiliar para hacer fetch con gestión de errores
 */
async function fetchAPI(endpoint, options = {}) {
    if (!CONFIG.USE_BACKEND) {
        console.warn(`⚠️ Backend deshabilitado. Usando mock data. Endpoint solicitado: ${endpoint}`);
        return null;
    }
    
    const url = `${CONFIG.API_BASE_URL}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CONFIG.FETCH_TIMEOUT);
    
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        console.error(`❌ Error en fetch: ${endpoint}`, error);
        throw error;
    }
}

/**
 * Cargar datos - automáticamente decide usar mock o backend
 */
async function loadData(mockData, endpoint) {
    if (CONFIG.USE_BACKEND) {
        try {
            return await fetchAPI(endpoint);
        } catch (error) {
            console.error(`Error cargando desde backend, usando mock data`);
            return mockData;
        }
    } else {
        // Usar mock data
        return mockData;
    }
}

console.log(`%c⚙️ SubSonic Festival Configuration`, "color: #00d4ff; font-weight: bold;");
console.log(`%cModo: ${CONFIG.USE_BACKEND ? "🔌 BACKEND" : "📦 MOCK DATA"}`, 
    `color: ${CONFIG.USE_BACKEND ? "#10b981" : "#ff006e"}; font-weight: bold;`);
console.log(`API Base URL: ${CONFIG.API_BASE_URL}`);
