(function renderEventoDetail() {
    const urlParams = new URLSearchParams(window.location.search);
    let eventId = urlParams.get('id');
    const cityName = urlParams.get('city');

    // Si viene un city pero no id, usar city como id
    if (!eventId && cityName) {
        eventId = cityName.toLowerCase().replace(/\s+/g, '');
    }

    if (!eventId) {
        window.location.href = 'eventos.html';
        return;
    }

    const data = window.EVENTOS_DATA;
    if (data) {
        fillEventoDetail(data, eventId);
        return;
    }

    fetch('eventos-data.json?t=' + Date.now() + Math.random(), { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar eventos-data.json (${response.status})`);
            }
            return response.json();
        })
        .then((fetchedData) => fillEventoDetail(fetchedData, eventId))
        .catch((error) => {
            console.error('Error al cargar evento:', error);
            window.location.href = 'eventos.html';
        });
})();

function fillEventoDetail(data, eventId) {
    const evento = (data.principales || []).find(e => e.id === eventId);

    if (!evento) {
        window.location.href = 'eventos.html';
        return;
    }

    // Encabezado del Evento
    const eventHeader = document.getElementById('eventHeader');
    if (eventHeader) {
        eventHeader.innerHTML = `
            <div class="event-detail-banner">
                <img src="${escapeHtml(evento.image)}" alt="${escapeHtml(evento.title)}" class="event-detail-image">
                <div class="event-detail-overlay">
                    <h1>${escapeHtml(evento.title)}</h1>
                    <p class="event-location-large">${escapeHtml(evento.location)}</p>
                </div>
            </div>
        `;
    }

    // Información del Evento
    const eventInfo = document.getElementById('eventInfo');
    if (eventInfo) {
        eventInfo.innerHTML = `
            <div class="info-details">
                <div class="info-detail-item">
                    <span class="detail-label">📅 Fecha:</span>
                    <span class="detail-value">${escapeHtml(evento.date)}</span>
                </div>
                <div class="info-detail-item">
                    <span class="detail-label">📍 Ubicación:</span>
                    <span class="detail-value">${escapeHtml(evento.location)}</span>
                </div>
                <div class="info-detail-item full-width">
                    <span class="detail-label">ℹ️ Descripción:</span>
                    <p class="detail-value">${escapeHtml(evento.description)}</p>
                </div>
            </div>
        `;
    }

    // Artistas
    const artistsList = document.getElementById('artistsList');
    if (artistsList) {
        const artists = evento.artists || [];
        let artistsHtml = '';

        // Verificar si es la nueva estructura (objeto con escenarios) o la antigua (array)
        if (Array.isArray(artists)) {
            // Estructura antigua: array de artistas
            artistsHtml = artists.map((artist) => `
                <div class="artist-list-item">
                    <div class="artist-info">
                        <h3>${escapeHtml(artist.name)}</h3>
                        <p class="artist-genre">${escapeHtml(artist.genre)}</p>
                        <p class="artist-time">🎤 ${escapeHtml(artist.time)}</p>
                    </div>
                    <button class="spotify-btn" title="Buscar en Spotify" data-url="${artist.spotify_url || ''}">
                        <img src="images/spotify-icon-spotify-social-media-logo-free-png.png" alt="Spotify" class="spotify-icon"/>
                    </button>
                </div>
            `).join('');
        } else {
            // Nueva estructura: objeto con escenarios
            const escenarios = ['Escenario 1', 'Escenario 2', 'Escenario 3'];
            escenarios.forEach((escenario) => {
                const escenarioArtists = artists[escenario] || [];
                if (escenarioArtists.length > 0) {
                    artistsHtml += `<div class="escenario-section"><h2 class="escenario-title">🎪 ${escapeHtml(escenario)}</h2>`;
                    artistsHtml += escenarioArtists.map((artist) => `
                        <div class="artist-list-item">
                            <div class="artist-info">
                                <h3>${escapeHtml(artist.name)}</h3>
                                <p class="artist-genre">${escapeHtml(artist.genre)}</p>
                                <p class="artist-time">🎤 ${escapeHtml(artist.time)}</p>
                            </div>
                            <button class="spotify-btn" title="Buscar en Spotify" data-url="${artist.spotify_url || ''}">
                                <img src="images/spotify-icon-spotify-social-media-logo-free-png.png" alt="Spotify" class="spotify-icon"/>
                            </button>
                        </div>
                    `).join('');
                    artistsHtml += '</div>';
                }
            });
        }

        artistsList.innerHTML = artistsHtml;
        
        // Agregar event listeners a los botones de Spotify
        const spotifyBtns = artistsList.querySelectorAll('.spotify-btn');
        spotifyBtns.forEach((btn, index) => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const artistName = btn.parentElement.querySelector('h3').textContent;
                // Usar siempre búsqueda por nombre (más confiable que IDs)
                const spotifyUrl = `https://open.spotify.com/search/${encodeURIComponent(artistName)}/artists`;
                window.open(spotifyUrl, '_blank');
            });
        });
    }

    // Entradas
    const ticketsGrid = document.getElementById('ticketsGrid');
    if (ticketsGrid) {
        const tickets = [
            {
                "title": "Entrada Individual",
                "price": "$65",
                "features": ["✓ Acceso 1 día", "✓ Acceso general", "✓ Programa del día"],
                "button": "Comprar Ahora",
                "featured": false
            },
            {
                "title": "Pase Completo",
                "price": "$120",
                "features": ["✓ 2 días de festival", "✓ Acceso a todos los escenarios", "✓ Programa completo", "✓ Descuento en food"],
                "button": "Comprar Ahora",
                "featured": true
            },
            {
                "title": "VIP Premium",
                "price": "$220",
                "features": ["✓ 2 días VIP", "✓ Área VIP exclusiva", "✓ Meet & Greet", "✓ Catering incluido"],
                "button": "Comprar Ahora",
                "featured": false
            }
        ];

        ticketsGrid.innerHTML = tickets.map((ticket) => {
            const cardClass = ticket.featured ? 'ticket-card featured' : 'ticket-card';
            const badge = '';
            const features = (ticket.features || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');

            return `
                <div class="${cardClass}">
                    ${badge}
                    <h3>${escapeHtml(ticket.title)}</h3>
                    <p class="price">${escapeHtml(ticket.price)}</p>
                    <ul class="ticket-features">${features}</ul>
                    <button class="btn-primary" onclick="procesarCompraEntrada('${escapeHtml(ticket.title)}', '${escapeHtml(ticket.price)}', '${escapeHtml(evento.title)}', '${escapeHtml(evento.location)}', '${escapeHtml(evento.date)}')">${escapeHtml(ticket.button)}</button>
                </div>
            `;
        }).join('');
    }
}

window.procesarCompraEntrada = function(titulo, precio, tituloEvento, ciudadEvento, fechaEvento) {
    if (window.authManager && window.authManager.getUser()) {
        const fallbackEvento = tituloEvento || "SUBSONIC Festival";
        const fallbackCiudad = ciudadEvento || "Ubicación Pendiente";
        const fallbackFecha = fechaEvento || "";
        window.location.href = `datos-bancarios.html?item=${encodeURIComponent(titulo)}&price=${encodeURIComponent(precio)}&evento=${encodeURIComponent(fallbackEvento)}&ciudad=${encodeURIComponent(fallbackCiudad)}&fecha=${encodeURIComponent(fallbackFecha)}`;
    } else {
        const currentUrl = window.location.href;
        window.location.href = `login.html?redirect=${encodeURIComponent(currentUrl)}`;
    }
};

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
