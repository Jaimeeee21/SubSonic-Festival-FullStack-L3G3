(function renderLoginView() {
    const data = window.LOGIN_DATA;
    if (data) {
        fillLogin(data);
        return;
    }

    fetch('login-data.json', { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar login-data.json (${response.status})`);
            }
            return response.json();
        })
        .then(fillLogin)
        .catch((error) => console.error('Error al cargar login-data:', error));
})();

function fillLogin(data) {
    const root = document.getElementById('authFormsRoot');
    if (!root) return;

    root.innerHTML = `
        <div class="auth-form" id="loginForm">
            <h2>${escapeHtml(data.login?.title || 'Iniciar Sesion')}</h2>
            <form>
                ${(data.login?.fields || []).map((field) => `
                    <div class="form-group">
                        <label for="${escapeHtml(field.id)}">${escapeHtml(field.label)}</label>
                        <input type="${escapeHtml(field.type)}" id="${escapeHtml(field.id)}" name="${escapeHtml(field.name)}" required>
                    </div>
                `).join('')}
                <button type="submit" class="btn-primary">${escapeHtml(data.login?.button || 'Iniciar Sesion')}</button>
            </form>
            <p class="toggle-auth">${escapeHtml(data.login?.toggleText || '')} <span onclick="toggleForms()">${escapeHtml(data.login?.toggleAction || '')}</span></p>
        </div>

        <div class="auth-form hidden" id="registerForm">
            <h2>${escapeHtml(data.register?.title || 'Crear Cuenta')}</h2>
            <form>
                ${(data.register?.fields || []).map((field) => `
                    <div class="form-group">
                        <label for="${escapeHtml(field.id)}">${escapeHtml(field.label)}</label>
                        <input type="${escapeHtml(field.type)}" id="${escapeHtml(field.id)}" name="${escapeHtml(field.name)}" required>
                    </div>
                `).join('')}
                <button type="submit" class="btn-primary">${escapeHtml(data.register?.button || 'Crear Cuenta')}</button>
            </form>
            <p class="toggle-auth">${escapeHtml(data.register?.toggleText || '')} <span onclick="toggleForms()">${escapeHtml(data.register?.toggleAction || '')}</span></p>
            <div class="business-link-section">
                <p class="business-text">${escapeHtml(data.register?.businessText || '')} <a href="${escapeHtml(data.register?.businessLinkHref || 'business-register.html')}" class="link-blue">${escapeHtml(data.register?.businessLinkText || '')}</a></p>
            </div>
        </div>
    `;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function toggleForms() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (loginForm && registerForm) {
        loginForm.classList.toggle('hidden');
        registerForm.classList.toggle('hidden');
    }
}
