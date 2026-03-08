(function renderCalendario() {
    const data = window.CALENDARIO_DATA;
    if (data) {
        fillCalendario(data);
        return;
    }

    fetch('calendario-data.json', { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar calendario-data.json (${response.status})`);
            }
            return response.json();
        })
        .then(fillCalendario)
        .catch((error) => console.error('Error al cargar calendario-data:', error));
})();

function fillCalendario(data) {
    renderTimeline('agostoTimeline', data.agosto || [], 'actual');
    renderTimeline('pasadoTimeline', data.pasado || [], 'pasado');
    renderTimeline('proximasTimeline', data.proximas || [], 'proximas');
}

function renderTimeline(containerId, events, eventType = 'actual') {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = events.map((item) => {
        // Extract city name for navigation
        const cityName = escapeHtml(item.location || item.title).split('-')[0].trim();
        let buttonHTML = '';

        // Renderizar botones según el tipo de evento
        if (eventType === 'actual') {
            // Eventos actuales: Solo botón "Comprar Entradas"
            const eventId = normalizeEventId(cityName);
            buttonHTML = `<button class="btn-primary" onclick="window.location.href='evento-detail.html?id=${eventId}'">Comprar Entradas</button>`;
        } else if (eventType === 'pasado') {
            // Eventos pasados: Solo botón "Ver Fotos"
            buttonHTML = `<button class="btn-primary" onclick="window.location.href='gallery.html?event=${encodeURIComponent(cityName)}'">Ver Fotos</button>`;
        } else if (eventType === 'proximas') {
            // Próximos eventos: Solo botón "Notificarme"
            buttonHTML = `<button class="btn-primary" onclick="showToast('¡Te notificaremos cuando estén disponibles las entradas!', 'success', 2500)" style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.5), rgba(131, 56, 236, 0.5)); border: 1px solid rgba(0, 212, 255, 0.4);">Notificarme</button>`;
        }
        
        return `
        <div class="timeline-event">
            <div class="event-date">
                <span class="day">${escapeHtml(item.day)}</span>
                <span class="month">${escapeHtml(item.month)}</span>
            </div>
            <div class="event-details">
                <h3>${escapeHtml(item.title)}</h3>
                <p class="event-location">${escapeHtml(item.location)}</p>
                <p class="event-description">${escapeHtml(item.description)}</p>
                <div style="display: flex; gap: 0.8rem; margin-top: 1rem;">
                    ${buttonHTML}
                </div>
            </div>
        </div>
    `;
    }).join('');
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Función para normalizar nombres de ciudades a IDs
function normalizeEventId(text) {
    return text
        .toLowerCase()
        .normalize('NFD')                   // Descompone caracteres acentuados
        .replace(/[\u0300-\u036f]/g, '')   // Remueve acentos
        .replace(/\s+/g, '');              // Remueve espacios
}
