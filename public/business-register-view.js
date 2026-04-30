(function renderBusinessRegister() {
    const data = window.BUSINESS_REGISTER_DATA;
    if (data) {
        fillBusinessRegister(data);
        return;
    }

    fetch('business-register-data.json', { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar business-register-data.json (${response.status})`);
            }
            return response.json();
        })
        .then(fillBusinessRegister)
        .catch((error) => console.error('Error al cargar business-register-data:', error));
})();

function fillBusinessRegister(data) {
    const root = document.getElementById('businessRegisterRoot');
    if (!root) return;

    const typeOptions = (data.businessTypes || []).map((item) => (
        `<option value="${escapeHtml(item.value)}">${escapeHtml(item.label)}</option>`
    )).join('');

    root.innerHTML = `
        <div class="auth-form" id="businessRegisterForm">
            <h2>${escapeHtml(data.title || '')}</h2>
            <p class="form-subtitle">${escapeHtml(data.subtitle || '')}</p>

            <form id="empresaForm">
                <div class="form-section-title">Informacion de la Empresa</div>
                <div class="form-group"><label for="companyName">Nombre de la Empresa:</label><input type="text" id="companyName" name="nombre" required></div>
                <div class="form-group"><label for="businessType">Tipo de Negocio:</label><select id="businessType" name="tipo_empresa" required>${typeOptions}</select></div>
                <div class="form-group"><label for="companyCIF">CIF/Registro:</label><input type="text" id="companyCIF" name="cif" placeholder="ej: B12345678" required></div>
                <div class="form-group"><label for="companyEmail">Correo Electronico de la Empresa:</label><input type="email" id="companyEmail" name="email_contacto" required></div>
                <div class="form-group"><label for="phone">Telefono de Contacto:</label><input type="tel" id="phone" name="telefono" required></div>
                <div class="form-group"><label for="companyDescription">Descripcion del Negocio:</label><textarea id="companyDescription" name="descripcion" placeholder="Cuentanos brevemente sobre tu empresa..." rows="4" required></textarea></div>
                <div class="form-group"><label for="website">Website (opcional):</label><input type="url" id="website" name="website" placeholder="https://"></div>

                <div class="form-section-title">Credenciales de Acceso</div>
                <p style="color:#666;font-size:0.9rem;margin:10px 0;">Tu empresa será accesible con el email registrado. Por favor verifica tu email después de registrarte.</p>
                
                <div class="form-group checkbox">
                    <input type="checkbox" id="terms" name="terms" required>
                    <label for="terms">Acepto los terminos y condiciones para empresas colaboradoras</label>
                </div>

                <div style="display:flex;gap:12px;">
                    <button type="submit" class="btn-primary">Registrar Empresa</button>
                </div>
            </form>

            <p class="toggle-auth">¿Eres usuario individual? <a href="login.html" class="link-blue">Vuelve al login</a></p>
            <p style="margin-top:8px;">¿Quieres reservar un espacio? <a href="reserve-space.html" class="link-blue">Ir a Reservar Espacio</a></p>
            <p style="margin-top:8px;border-top:1px solid #ddd;padding-top:12px;"><strong>¿Ya eres empresa?</strong> <a href="business-login.html" class="link-blue">Inicia sesión aquí</a></p>
        </div>
    `;
    
    // Agregar manejador de submit
    const form = document.getElementById('empresaForm');
    if (form) {
        form.addEventListener('submit', handleEmpresaRegistro);
    }
}

async function handleEmpresaRegistro(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Validar que las contraseñas coincidan
    const terms = document.getElementById('terms').checked;
    if (!terms) {
        alert('Debes aceptar los términos y condiciones');
        return;
    }
    
    // Convertir formData a objeto con validación de tipos
    const datos = {
        nombre: String(formData.get('nombre')).trim(),
        cif: String(formData.get('cif')).trim(),
        tipo_empresa: String(formData.get('tipo_empresa')).trim(),
        descripcion: String(formData.get('descripcion')).trim(),
        telefono: String(formData.get('telefono')).trim(),
        email_contacto: String(formData.get('email_contacto')).trim(),
        website: formData.get('website') ? String(formData.get('website')).trim() : "",
        logo_url: ""
    };
    
    // Validar campos requeridos
    if (!datos.nombre || !datos.cif || !datos.tipo_empresa || !datos.descripcion || !datos.telefono || !datos.email_contacto) {
        alert('❌ Por favor completa todos los campos requeridos');
        return;
    }
    
    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(datos.email_contacto)) {
        alert('❌ Email inválido');
        return;
    }
    
    console.log('Datos a enviar:', datos);
    
    // Mostrar loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Registrando...';
    
    try {
        const response = await fetch('http://pil3g3.duckdns.org/api/empresas/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });
        
        const result = await response.json();
        console.log('Respuesta del servidor:', response.status, result);
        
        if (response.ok) {
            alert('✅ ¡Empresa registrada exitosamente!\n\n' +
                  'Nombre: ' + datos.nombre + '\n' +
                  'Email: ' + datos.email_contacto + '\n\n' +
                  'Serás redirigido a la vista de empresas...');
            
            // Guardar token temporal
            localStorage.setItem('empresa_token', datos.email_contacto);
            
            // Redirigir a la vista de empresas
            setTimeout(() => {
                window.location.href = 'index-business.html';
            }, 1500);
        } else {
            // Extraer mensaje de error
            let mensajeError = 'Error desconocido';
            if (result.detail) {
                if (typeof result.detail === 'string') {
                    mensajeError = result.detail;
                } else if (Array.isArray(result.detail)) {
                    mensajeError = result.detail.map(e => e.msg || e.message || JSON.stringify(e)).join('\n');
                } else {
                    mensajeError = JSON.stringify(result.detail);
                }
            }
            alert('❌ Error en registro:\n' + mensajeError);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error de conexión: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
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
