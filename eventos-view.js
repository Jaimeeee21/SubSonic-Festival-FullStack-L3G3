(function renderEventos() {
    const data = window.EVENTOS_DATA;
    if (data) {
        fillEventos(data);
        return;
    }

    fetch('eventos-data.json?t=' + Date.now() + Math.random(), { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar eventos-data.json (${response.status})`);
            }
            return response.json();
        })
        .then(fillEventos)
        .catch((error) => console.error('Error al cargar eventos-data:', error));
})();

function fillEventos(data) {
    const principalesGrid = document.getElementById('principalesGrid');

    if (principalesGrid) {
        principalesGrid.innerHTML = (data.principales || []).map((item) => `
            <div class="event-list-item">
                <div class="event-content">
                    <h3>${escapeHtml(item.title)}</h3>
                    <div class="event-details">
                        ${(item.info || []).map((line) => `<span class="info-item">${escapeHtml(line)}</span>`).join('')}
                    </div>
                    <p class="event-desc">${escapeHtml(item.description)}</p>
                </div>
                <a href="evento-detail.html?id=${escapeHtml(item.id)}" class="btn-event-buy">Comprar Entrada</a>
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
