/**
 * EJEMPLO COMPLETO: eventos-data.js adaptado para usar backend o mock
 * 
 * Este archivo muestra cómo cambiar solo una variable (CONFIG.USE_BACKEND)
 * para usar el backend real o mock data.
 * 
 * Nota: Este es un EJEMPLO. El archivo actual eventos-data.js.bak conserva
 * la versión original. Cuando estés listo, renombra este archivo a eventos-data.js
 * y elimina el .bak
 */

// Esperar a que config.js esté cargado
if (typeof CONFIG === 'undefined') {
    console.error('❌ config.js no está cargado. Asegúrate de cargar config.js ANTES de eventos-data.js');
}

/**
 * Función principal: Cargar datos de eventos
 * Automáticamente decide si usar backend o mock basado en CONFIG.USE_BACKEND
 */
(function initEventosData() {
    console.log(`📊 Cargando eventos (Modo: ${CONFIG.USE_BACKEND ? 'BACKEND 🔌' : 'MOCK 📦'})`);
    
    if (CONFIG.USE_BACKEND) {
        loadEventosFromBackend();
    } else {
        loadEventosFromMock();
    }
})();

/**
 * Cargar eventos desde el backend API
 */
function loadEventosFromBackend() {
    const endpoint = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventos;
    
    fetch(endpoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(eventosArray => {
        // Transformar respuesta del backend al formato que espera el frontend
        window.EVENTOS_DATA = transformEventosFromBackend(eventosArray);
        console.log('✅ Eventos cargados desde backend:', window.EVENTOS_DATA);
        
        // Disponer evento para que las vistas se actualicen
        document.dispatchEvent(new CustomEvent('eventosActualizados', { detail: window.EVENTOS_DATA }));
    })
    .catch(error => {
        console.error('❌ Error cargando eventos del backend:', error);
        console.warn('⚠️ Fallback: Usando mock data...');
        loadEventosFromMock();
    });
}

/**
 * Cargar eventos desde JSON mock local
 */
function loadEventosFromMock() {
    const url = 'eventos-data.json?t=' + Date.now() + Math.random();
    
    fetch(url, { cache: 'no-store' })
    .then(response => {
        if (!response.ok) {
            throw new Error(`No se pudo cargar eventos-data.json (${response.status})`);
        }
        return response.json();
    })
    .then(data => {
        window.EVENTOS_DATA = data;
        console.log('✅ Eventos cargados desde mock:', window.EVENTOS_DATA);
        
        document.dispatchEvent(new CustomEvent('eventosActualizados', { detail: window.EVENTOS_DATA }));
    })
    .catch(error => console.error('❌ Error al cargar eventos:', error));
}

/**
 * Transformar respuesta del backend al formato esperado por el frontend
 * 
 * Backend devuelve:
 * [
 *   {
 *     id: "madrid",
 *     titulo: "SUBSONIC 2026",
 *     fecha: "15-17 Agosto",
 *     ubicacion: "Madrid",
 *     descripcion: "...",
 *     imagen_url: "...",
 *     capacidad: 50000,
 *     artistas: {...},
 *     info: [...]
 *   },
 *   ...
 * ]
 * 
 * Frontend espera:
 * {
 *   "principales": [
 *     {
 *       id: "madrid",
 *       title: "SUBSONIC 2026",
 *       date: "15-17 Agosto",
 *       ...
 *     }
 *   ]
 * }
 */
function transformEventosFromBackend(eventosArray) {
    if (!Array.isArray(eventosArray)) {
        console.error('❌ Respuesta no es un array:', eventosArray);
        return { principales: [] };
    }
    
    return {
        principales: eventosArray.map(evento => ({
            id: evento.id,
            title: evento.titulo,
            date: evento.fecha,
            location: evento.ubicacion,
            description: evento.descripcion,
            image: evento.imagen_url,
            info: evento.info || [],
            artists: evento.artistas || [],
            capacity: evento.capacidad || null
        }))
    };
}

/**
 * Funciones auxiliares para interactuar con eventos desde las vistas
 */

/**
 * Obtener un evento específico por ID
 */
async function obtenerEvento(eventoId) {
    if (CONFIG.USE_BACKEND) {
        const endpoint = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventos + `/${eventoId}`;
        
        try {
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`❌ Error obteniendo evento ${eventoId}:`, error);
            // Fallback: buscar en mock data
            return window.EVENTOS_DATA?.principales?.find(e => e.id === eventoId);
        }
    } else {
        // Con mock: solo buscar en la estructura de datos
        return window.EVENTOS_DATA?.principales?.find(e => e.id === eventoId);
    }
}

/**
 * Obtener eventos filtrados por ubicación
 */
async function obtenerEventosPorUbicacion(ubicacion) {
    if (CONFIG.USE_BACKEND) {
        const endpoint = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventosPorUbicacion(ubicacion);
        
        try {
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`❌ Error obteniendo eventos por ubicación:`, error);
            // Fallback
            return window.EVENTOS_DATA?.principales?.filter(e => e.location === ubicacion) || [];
        }
    } else {
        // Con mock
        return window.EVENTOS_DATA?.principales?.filter(e => e.location === ubicacion) || [];
    }
}

/**
 * Crear un nuevo evento (solo disponible con backend)
 */
async function crearEvento(datosEvento) {
    if (!CONFIG.USE_BACKEND) {
        console.warn('⚠️ Crear eventos solo está disponible con backend habilitado');
        return null;
    }
    
    const endpoint = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventos;
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datosEvento)
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const nuevoEvento = await response.json();
        console.log('✅ Evento creado:', nuevoEvento);
        
        // Recargar eventos
        loadEventosFromBackend();
        
        return nuevoEvento;
    } catch (error) {
        console.error('❌ Error creando evento:', error);
        return null;
    }
}

/**
 * Actualizar un evento
 */
async function actualizarEvento(eventoId, datosActualizados) {
    if (!CONFIG.USE_BACKEND) {
        console.warn('⚠️ Actualizar eventos solo está disponible con backend habilitado');
        return null;
    }
    
    const endpoint = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventos + `/${eventoId}`;
    
    try {
        const response = await fetch(endpoint, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datosActualizados)
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const eventoActualizado = await response.json();
        console.log('✅ Evento actualizado:', eventoActualizado);
        
        // Recargar eventos
        loadEventosFromBackend();
        
        return eventoActualizado;
    } catch (error) {
        console.error('❌ Error actualizando evento:', error);
        return null;
    }
}

/**
 * Eliminar un evento
 */
async function eliminarEvento(eventoId) {
    if (!CONFIG.USE_BACKEND) {
        console.warn('⚠️ Eliminar eventos solo está disponible con backend habilitado');
        return false;
    }
    
    const endpoint = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.eventos + `/${eventoId}`;
    
    try {
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        console.log('✅ Evento eliminado:', eventoId);
        
        // Recargar eventos
        loadEventosFromBackend();
        
        return true;
    } catch (error) {
        console.error('❌ Error eliminando evento:', error);
        return false;
    }
}

console.log('%c✨ eventos-data.js cargado (frontend/backend flexible)', 'color: #10b981; font-weight: bold;');
