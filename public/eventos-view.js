(async function renderEventos() {
    let data;
    
    if (CONFIG.USE_BACKEND) {
        try {
            console.log("📡 Cargando eventos desde backend...");
            const eventosBackend = await fetchAPI(CONFIG.ENDPOINTS.eventos);
            
            if (eventosBackend && Array.isArray(eventosBackend)) {
                // Transformar datos del backend al formato esperado
                data = {
                    principales: eventosBackend.map(evento => ({
                        id: evento.id,
                        title: evento.titulo || evento.title || "Sin título",
                        date: evento.fecha || "Fecha no disponible",
                        location: evento.ubicacion || evento.location || "Ubicación no disponible",
                        description: evento.descripcion || evento.description || "Sin descripción",
                        image: evento.imagen_url || evento.image || "https://via.placeholder.com/400x300",
                        info: Array.isArray(evento.info) ? 
                            evento.info.map(inf => `ℹ️ ${inf}`) : 
                            [`📍 ${evento.ubicacion || evento.location}`, `📅 ${evento.fecha || evento.date}`],
                        artists: Array.isArray(evento.artistas) ? 
                            {"Artistas": evento.artistas.map(a => ({name: a, genre: "Temas especiales"}))} :
                            evento.artists || {}
                    }))
                };
                console.log("✅ Eventos cargados desde backend:", data);
            }
        } catch (error) {
            console.error("❌ Error cargando desde backend, usando mock data:", error);
        }
    }
    
    // Si no se cargó desde backend, usar mock data
    if (!data) {
        data = window.EVENTOS_DATA;
        if (!data) {
            try {
                const response = await fetch('eventos-data.json?t=' + Date.now() + Math.random(), { cache: 'no-store' });
                if (response.ok) {
                    data = await response.json();
                    console.log("📦 Eventos cargados desde archivo mock");
                } else {
                    throw new Error(`HTTP ${response.status}`);
                }
            } catch (error) {
                console.error('❌ Error al cargar eventos-data:', error);
                data = { principales: [] };
            }
        } else {
            console.log("📦 Usando EVENTOS_DATA definido globalmente");
        }
    }
    
    if (data) {
        fillEventos(data);
    }
})();

function fillEventos(data) {
    const principalesGrid = document.getElementById('principalesGrid');

    if (principalesGrid) {
        principalesGrid.innerHTML = (data.principales || []).map((item) => `
            <div class="event-list-item" onclick="window.location.href='evento-detail.html?id=${escapeHtml(item.id)}'" style="cursor: pointer;">
                <div class="event-content">
                    <h3>${escapeHtml(item.title)}</h3>
                    <div class="event-details">
                        ${(item.info || []).map((line) => `<span class="info-item">${escapeHtml(line)}</span>`).join('')}
                    </div>
                    <p class="event-desc">${escapeHtml(item.description)}</p>
                </div>
                <a href="evento-detail.html?id=${escapeHtml(item.id)}" class="btn-event-buy" onclick="event.stopPropagation();">Comprar Entrada</a>
            </div>
        `).join('');
    }
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
