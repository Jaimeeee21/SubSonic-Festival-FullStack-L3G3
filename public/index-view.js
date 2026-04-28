(function renderIndexView() {
    const data = window.INDEX_DATA;
    if (data) {
        fillIndex(data);
        return;
    }

    fetch('index-data.json', { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar index-data.json (${response.status})`);
            }
            return response.json();
        })
        .then(fillIndex)
        .catch((error) => {
            console.error('Error al cargar index-data:', error);
        });
})();

function fillIndex(data) {
    const carouselTrack = document.getElementById('carouselTrack');
    const artistsGrid = document.querySelector('.artists-grid');
    const infoGrid = document.querySelector('.info-grid');
    const ticketsGrid = document.querySelector('.tickets-grid');

    if (carouselTrack) {
        carouselTrack.innerHTML = (data.carouselSlides || []).map((slide) => `
            <div class="event-card">
                <img src="${escapeHtml(slide.image)}" alt="${escapeHtml(slide.alt || slide.title)}" class="event-img">
                <div class="event-overlay">
                    <h2>${escapeHtml(slide.title)}</h2>
                    <p class="event-date">${escapeHtml(slide.date)}</p>
                    <p class="event-description">${escapeHtml(slide.description)}</p>
                </div>
            </div>
        `).join('');
    }

    if (artistsGrid) {
        artistsGrid.innerHTML = (data.artists || []).map((artist) => `
            <div class="artist-card" data-genre="${escapeHtml(artist.dataGenre || '')}">
                <div class="artist-image">${escapeHtml(artist.icon)}</div>
                <h3>${escapeHtml(artist.name)}</h3>
                <p class="genre">${escapeHtml(artist.genre)}</p>
                <p class="date">${escapeHtml(artist.date)}</p>
            </div>
        `).join('');
    }

    if (infoGrid) {
        infoGrid.innerHTML = (data.infoCards || []).map((card) => {
            const normalLines = (card.lines || []).slice(0, -1).map((line) => `<p>${escapeHtml(line)}</p>`).join('');
            const lastLine = card.lines?.length ? `<p class="small-text">${escapeHtml(card.lines[card.lines.length - 1])}</p>` : '';

            return `
                <div class="info-card">
                    <div class="info-icon">${escapeHtml(card.icon)}</div>
                    <h3>${escapeHtml(card.title)}</h3>
                    ${normalLines}
                    ${lastLine}
                </div>
            `;
        }).join('');
    }

    if (ticketsGrid) {
        ticketsGrid.innerHTML = (data.tickets || []).map((ticket) => {
            const cardClass = ticket.featured ? 'ticket-card featured' : 'ticket-card';
            const buttonClass = ticket.featured ? 'ticket-button featured-button' : 'ticket-button';
            const badge = ticket.featured && ticket.badge ? `<span class="badge">${escapeHtml(ticket.badge)}</span>` : '';
            const features = (ticket.features || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');

            return `
                <div class="${cardClass}">
                    ${badge}
                    <h3>${escapeHtml(ticket.title)}</h3>
                    <p class="price">${escapeHtml(ticket.price)}</p>
                    <ul class="ticket-features">${features}</ul>
                    <button class="${buttonClass}">${escapeHtml(ticket.button)}</button>
                </div>
            `;
        }).join('');
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
