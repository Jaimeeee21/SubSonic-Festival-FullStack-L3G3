// Renderizar formulario de login de empresa
(function renderBusinessLogin() {
    const root = document.getElementById('businessLoginRoot');
    if (!root) return;

    root.innerHTML = `
        <div class="auth-form" id="businessLoginForm">
            <h2>Iniciar Sesión - Empresa</h2>

            <form id="loginEmpresaForm">
                <div class="form-group">
                    <label for="empresaEmail">Email de la Empresa:</label>
                    <input type="email" id="empresaEmail" name="email" placeholder="tu-empresa@email.com" required>
                </div>

                <div class="form-group checkbox">
                    <input type="checkbox" id="recuerdame" name="recuerdame">
                    <label for="recuerdame">Recuérdame en este dispositivo</label>
                </div>

                <button type="submit" class="btn-primary">Acceder a Mi Panel</button>
            </form>

            <p class="toggle-auth">¿Aún no eres empresa? <a href="business-register.html" class="link-blue">Regístrate aquí</a></p>
            <p class="toggle-auth">¿Eres usuario individual? <a href="login.html" class="link-blue">Vuelve al login</a></p>
        </div>
    `;
    
    // Agregar manejador de submit
    const form = document.getElementById('loginEmpresaForm');
    if (form) {
        form.addEventListener('submit', handleEmpresaLogin);
    }
})();

async function handleEmpresaLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const email = document.getElementById('empresaEmail').value.trim();
    const recuerdame = document.getElementById('recuerdame').checked;
    
    if (!email) {
        alert('❌ Por favor ingresa el email de tu empresa');
        return;
    }
    
    console.log('Intentando login con email:', email);
    
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Validando...';
    
    try {
        // Hacer login al endpoint de autenticación para empresas
        const response = await fetch('http://pil3g3.duckdns.org/api/auth/login-email-business', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: ""  // No requerido para empresas
            })
        });
        
        const result = await response.json();
        console.log('Respuesta del servidor:', response.status, result);
        
        if (response.ok && result.token) {
            // Guardar token
            localStorage.setItem('auth_token', result.token);
            localStorage.setItem('empresa_nombre', result.empresa_nombre || 'Empresa');
            localStorage.setItem('usuario_id', result.usuario_id || '');
            localStorage.setItem('empresa_id', result.empresa_id || '');

            // Guardar datos en userName para el navbar (nombre de empresa)
            localStorage.setItem('userName', result.empresa_nombre || 'Empresa');
            localStorage.setItem('isEmpresa', 'true');

            if (recuerdame) {
                localStorage.setItem('empresa_email_recordada', email);
            }

            alert('✅ ¡Sesión iniciada correctamente!\n\n' +
                  'Empresa: ' + (result.empresa_nombre || 'Empresa') + '\n\n' +
                  'Serás redirigido a tu panel...');

            // Redirigir al panel de empresa
            setTimeout(() => {
                window.location.href = 'index-business.html';
            }, 1500);
        } else {
            let mensajeError = 'Email o empresa no encontrada';
            if (result.detail) {
                if (typeof result.detail === 'string') {
                    mensajeError = result.detail;
                } else {
                    mensajeError = JSON.stringify(result.detail);
                }
            }
            alert('❌ Error en login:\n' + mensajeError);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// Recuperar email recordado si existe
window.addEventListener('load', function() {
    const emailRecordada = localStorage.getItem('empresa_email_recordada');
    if (emailRecordada) {
        const emailInput = document.getElementById('empresaEmail');
        if (emailInput) {
            emailInput.value = emailRecordada;
        }
        const recuerdameCheckbox = document.getElementById('recuerdame');
        if (recuerdameCheckbox) {
            recuerdameCheckbox.checked = true;
        }
    }
});
