let reserveSpaceData = window.RESERVE_SPACE_DATA || {};
let availabilityData = {};
let selectedEvent = '';
let selectedEventName = '';
let selectedSpace = '';
let selectedSpaceName = '';

// Obtener modo desde parámetros de URL (mock o real)
function getDataMode() {
    const params = new URLSearchParams(window.location.search);
    return params.get('mode') || 'mock'; // Por defecto 'mock'
}

const dataMode = getDataMode();
console.log('Modo de datos:', dataMode);

(async function initReserveSpace() {
    if (dataMode === 'real') {
        await loadFromBackend();
    } else {
        await loadFromMock();
    }

    renderEvents();
    
    // Inicializar disponibilidad con el primer evento
    if (reserveSpaceData.events && reserveSpaceData.events.length > 0) {
        updateAvailabilityForEvent(reserveSpaceData.events[0].id);
    }
    
    renderSpaces();

    const reserveForm = document.getElementById('reserveForm');
    if (reserveForm) {
        reserveForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const eventData = (reserveSpaceData.events || []).find((item) => item.id === selectedEvent);
            alert('Solicitud enviada para ' + selectedEventName + ' (' + (eventData?.duration || '') + ')\nEspacio: ' + selectedSpaceName + '\nTe contactaremos pronto.');
            reserveForm.reset();
            backToEvents();
        });
    }
})();

async function loadFromMock() {
    console.log('Cargando datos desde MOCK (JSONs locales)...');
    
    // Primero intentar cargar eventos desde eventos-data.json
    try {
        const response = await fetch('eventos-data.json?t=' + Date.now() + Math.random(), { cache: 'no-store' });
        if (response.ok) {
            const eventosData = await response.json();
            if (eventosData.principales && eventosData.principales.length > 0) {
                // Convertir eventos al formato necesario para reserve-space
                reserveSpaceData.events = eventosData.principales.map((evento) => {
                    // Calcular número de días
                    const dateParts = evento.date.split('-');
                    const startDay = parseInt(dateParts[0]);
                    const endDay = parseInt(dateParts[1]);
                    const numDias = endDay - startDay + 1;
                    const diasText = numDias === 1 ? '1 dia completo' : numDias + ' dias completos';
                    
                    // Colores variados para los eventos
                    const colors = ['#6b21a8', '#00d4ff', '#ff006e', '#10b981', '#f59e0b', '#8b5cf6'];
                    const colorIndex = eventosData.principales.indexOf(evento) % colors.length;
                    
                    return {
                        id: evento.id,
                        name: `SUBSONIC 2026 - ${evento.location}`,
                        icon: '🎵',
                        dates: evento.date,
                        duration: evento.date + ' (' + diasText + ')',
                        summary: evento.location + ' - ' + evento.description.substring(0, 60) + '...',
                        accent: colors[colorIndex]
                    };
                });
            }
        }
    } catch (error) {
        console.error('Error al cargar eventos-data.json:', error);
    }
    
    // Cargar espacios desde reserve-space-data.json
    try {
        const response = await fetch('reserve-space-data.json', { cache: 'no-store' });
        if (response.ok) {
            const spaceData = await response.json();
            if (spaceData.spaces) {
                reserveSpaceData.spaces = spaceData.spaces;
            }
            if (spaceData.messages) {
                reserveSpaceData.messages = spaceData.messages;
            }
        }
    } catch (error) {
        console.error('Error al cargar reserve-space-data:', error);
    }

    // Cargar disponibilidad desde reserve-space-availability.json
    try {
        const response = await fetch('reserve-space-availability.json', { cache: 'no-store' });
        if (response.ok) {
            availabilityData = await response.json();
        }
    } catch (error) {
        console.warn('Advertencia: No se pudo cargar reserve-space-availability.json, usando valores por defecto:', error);
    }
}

async function loadFromBackend() {
    console.log('Cargando datos desde BACKEND...');
    
    // TODO: Configurar los endpoints del backend según sea necesario
    const backendUrl = 'http://localhost:3000/api'; // Cambiar por URL real del backend
    
    // Ejemplo de estructura esperada desde el backend:
    // GET /api/eventos - devuelve eventos
    // GET /api/espacios - devuelve espacios
    // GET /api/disponibilidad - devuelve disponibilidad
    
    try {
        // Cargar eventos del backend
        const eventosResponse = await fetch(backendUrl + '/eventos', { cache: 'no-store' });
        if (eventosResponse.ok) {
            const eventosData = await eventosResponse.json();
            if (eventosData.principales && eventosData.principales.length > 0) {
                reserveSpaceData.events = eventosData.principales.map((evento) => {
                    const dateParts = evento.date.split('-');
                    const startDay = parseInt(dateParts[0]);
                    const endDay = parseInt(dateParts[1]);
                    const numDias = endDay - startDay + 1;
                    const diasText = numDias === 1 ? '1 dia completo' : numDias + ' dias completos';
                    
                    const colors = ['#6b21a8', '#00d4ff', '#ff006e', '#10b981', '#f59e0b', '#8b5cf6'];
                    const colorIndex = eventosData.principales.indexOf(evento) % colors.length;
                    
                    return {
                        id: evento.id,
                        name: `SUBSONIC 2026 - ${evento.location}`,
                        icon: '🎵',
                        dates: evento.date,
                        duration: evento.date + ' (' + diasText + ')',
                        summary: evento.location + ' - ' + evento.description.substring(0, 60) + '...',
                        accent: colors[colorIndex]
                    };
                });
            }
        }
    } catch (error) {
        console.error('Error al cargar eventos del backend:', error);
    }
    
    try {
        // Cargar espacios del backend
        const spacesResponse = await fetch(backendUrl + '/espacios', { cache: 'no-store' });
        if (spacesResponse.ok) {
            const spaceData = await spacesResponse.json();
            if (spaceData.spaces) {
                reserveSpaceData.spaces = spaceData.spaces;
            }
            if (spaceData.messages) {
                reserveSpaceData.messages = spaceData.messages;
            }
        }
    } catch (error) {
        console.error('Error al cargar espacios del backend:', error);
    }
    
    try {
        // Cargar disponibilidad del backend
        const availResponse = await fetch(backendUrl + '/disponibilidad', { cache: 'no-store' });
        if (availResponse.ok) {
            availabilityData = await availResponse.json();
        }
    } catch (error) {
        console.warn('Advertencia: No se pudo cargar disponibilidad del backend:', error);
    }
}

function renderEvents() {
    const eventsGrid = document.getElementById('eventsGrid');
    if (!eventsGrid) return;

    eventsGrid.innerHTML = (reserveSpaceData.events || []).map((item) => `
        <div class="event-card" data-event-id="${escapeHtml(item.id)}" onclick="selectEvent('${escapeHtml(item.id)}')" style="background:#fff;padding:24px;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,0.06);border:2px solid transparent;cursor:pointer;transition:all 0.3s ease;">
            <h3 style="margin:0 0 12px 0;color:${escapeHtml(item.accent)};">${escapeHtml(item.icon)} ${escapeHtml(item.name)}</h3>
            <p style="margin:0;color:#666;font-size:0.95rem;">${escapeHtml(item.dates)}</p>
            <p style="margin:8px 0 0 0;color:#888;font-size:0.85rem;">✓ ${escapeHtml(item.duration.split('(')[1]?.replace(')', '') || '')}</p>
            <p style="margin:12px 0 0 0;color:#888;font-size:0.85rem;">${escapeHtml(item.summary)}</p>
        </div>
    `).join('');
}

function renderSpaces() {
    const spacesGrid = document.getElementById('spacesGrid');
    if (!spacesGrid) return;

    spacesGrid.innerHTML = (reserveSpaceData.spaces || []).map((item) => {
        const opacity = item.available ? '1' : '0.6';
        return `
            <div class="space-card" data-space-id="${escapeHtml(item.id)}" onclick="selectSpace('${escapeHtml(item.id)}')" style="background:#fff;padding:24px;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,0.06);border-left:4px solid ${escapeHtml(item.accent)};cursor:pointer;transition:all 0.3s ease;opacity:${opacity};">
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:12px;">
                    <h3 style="margin:0;color:${escapeHtml(item.accent)};">${escapeHtml(item.icon)} ${escapeHtml(item.name)}</h3>
                    <span style="background:${escapeHtml(item.statusColor)};color:white;padding:4px 12px;border-radius:16px;font-size:0.8rem;font-weight:600;">${escapeHtml(item.statusText)}</span>
                </div>
                <p style="font-size:1.2rem;font-weight:600;color:#333;margin:10px 0;">${escapeHtml(item.size)}</p>
                <p style="font-size:0.9rem;color:#666;margin:8px 0;"><strong>Espacios disponibles:</strong> ${escapeHtml(item.availability)}</p>
                <ul style="list-style:none;padding:0;margin:12px 0;color:#666;font-size:0.95rem;">
                    ${(item.features || []).map((line) => `<li style="padding:6px 0;">${escapeHtml(line)}</li>`).join('')}
                </ul>
                <p style="font-size:0.9rem;color:#888;margin-bottom:0;">${escapeHtml(item.description)}</p>
            </div>
        `;
    }).join('');
}

function updateAvailabilityForEvent(eventId) {
    if (!availabilityData.availability || !availabilityData.availability[eventId]) {
        return; // Si no hay datos de disponibilidad para este evento, mantener valores por defecto
    }

    const eventAvailability = availabilityData.availability[eventId];
    
    // Actualizar disponibilidad de espacios
    (reserveSpaceData.spaces || []).forEach((space) => {
        const availInfo = eventAvailability.find((item) => item.id === space.id);
        if (availInfo) {
            space.availability = availInfo.available + ' de ' + availInfo.total;
            space.available = availInfo.available > 0;
            
            // Actualizar estado visual: si hay 3 o menos disponibles = pocas quedan
            if (availInfo.available === 0) {
                space.statusText = '✗ Agotado';
                space.statusColor = '#ef4444';
            } else if (availInfo.available <= 3) {
                space.statusText = '⚠ Pocas quedan';
                space.statusColor = '#f59e0b';
            } else {
                space.statusText = '✓ Disponible';
                space.statusColor = '#10b981';
            }
        }
    });
}

function selectEvent(eventId) {
    const eventData = (reserveSpaceData.events || []).find((item) => item.id === eventId);
    if (!eventData) return;

    selectedEvent = eventId;
    selectedEventName = eventData.name;

    // Actualizar disponibilidad de espacios para el evento seleccionado
    updateAvailabilityForEvent(eventId);

    document.getElementById('selectedEventName').textContent = eventData.name;
    document.getElementById('selectedEventDisplay').textContent = eventData.name;
    document.getElementById('eventDurationInfo').textContent = 'Duracion: ' + eventData.duration;

    document.querySelectorAll('.event-card').forEach((card) => {
        card.style.borderColor = 'transparent';
        card.style.backgroundColor = '#fff';
    });

    const selectedCard = document.querySelector(`[data-event-id="${eventId}"]`);
    if (selectedCard) {
        selectedCard.style.borderColor = '#00d4ff';
        selectedCard.style.backgroundColor = '#f0f9ff';
    }

    document.getElementById('eventsSection').style.display = 'none';
    document.getElementById('spacesSection').style.display = 'block';
    document.getElementById('formSection').style.display = 'none';
    window.scrollTo(0, 0);
}

function selectSpace(spaceId) {
    const spaceData = (reserveSpaceData.spaces || []).find((item) => item.id === spaceId);
    if (!spaceData) return;

    if (!spaceData.available) {
        alert(reserveSpaceData.messages?.soldOut || 'Lo sentimos, este espacio esta agotado.');
        return;
    }

    selectedSpace = spaceId;
    selectedSpaceName = `${spaceData.name} (${spaceData.size})`;
    document.getElementById('selectedSpaceDisplay').textContent = selectedSpaceName;

    document.querySelectorAll('.space-card').forEach((card) => {
        card.style.backgroundColor = '#fff';
    });

    const selectedCard = document.querySelector(`[data-space-id="${spaceId}"]`);
    if (selectedCard) {
        selectedCard.style.backgroundColor = '#f0f9ff';
    }

    document.getElementById('eventsSection').style.display = 'none';
    document.getElementById('spacesSection').style.display = 'none';
    document.getElementById('formSection').style.display = 'block';
    window.scrollTo(0, 0);
}

function backToEvents() {
    selectedEvent = '';
    selectedEventName = '';
    selectedSpace = '';
    selectedSpaceName = '';
    document.getElementById('eventsSection').style.display = 'block';
    document.getElementById('spacesSection').style.display = 'none';
    document.getElementById('formSection').style.display = 'none';
    window.scrollTo(0, 0);
}

function backToSpaces() {
    selectedSpace = '';
    selectedSpaceName = '';
    document.getElementById('eventsSection').style.display = 'none';
    document.getElementById('spacesSection').style.display = 'block';
    document.getElementById('formSection').style.display = 'none';
    window.scrollTo(0, 0);
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
