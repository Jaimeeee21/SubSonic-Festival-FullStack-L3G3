(function renderFaqView() {
    if (window.FAQ_DATA && Object.keys(window.FAQ_DATA).length > 0) {
        fillFaq(window.FAQ_DATA);
        return;
    }

    fetch('faq-data.json', { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar faq-data.json (${response.status})`);
            }
            return response.json();
        })
        .then(fillFaq)
        .catch((error) => console.error('Error al cargar faq-data:', error));
})();

function fillFaq(data) {
    renderFaqList('eventoFaqList', data.evento || []);
    renderFaqList('fechasFaqList', data.fechas || []);
    renderFaqList('merchFaqList', data.merch || []);

    const contactInfoList = document.getElementById('contactInfoList');
    if (contactInfoList) {
        contactInfoList.innerHTML = (data.contactInfo || []).map((item) => {
            let content = '';
            if (item.isEmail) {
                content = `<a href="mailto:${escapeHtml(item.value)}">${escapeHtml(item.value)}</a>`;
            } else if (item.allowHtml) {
                content = item.value;
            } else {
                content = escapeHtml(item.value);
            }

            return `
                <div class="contact-item">
                    <span class="contact-icon">${escapeHtml(item.icon)}</span>
                    <div>
                        <h4>${escapeHtml(item.title)}</h4>
                        <p>${content}</p>
                    </div>
                </div>
            `;
        }).join('');
    }
}

function renderFaqList(containerId, items) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = items.map((item) => `
        <div class="faq-item">
            <button class="faq-question">
                <span>${escapeHtml(item.q)}</span>
                <i class="fas fa-chevron-down"></i>
            </button>
            <div class="faq-answer">
                <p>${escapeHtml(item.a)}</p>
            </div>
        </div>
    `).join('');
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
