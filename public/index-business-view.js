(function renderIndexBusiness() {
    const data = window.INDEX_BUSINESS_DATA;
    if (data) {
        fillIndexBusiness(data);
        cargarEmpresaYReservas();
        return;
    }

    fetch('index-business-data.json', { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar index-business-data.json (${response.status})`);
            }
            return response.json();
        })
        .then((data) => {
            fillIndexBusiness(data);
            cargarEmpresaYReservas();
        })
        .catch((error) => console.error('Error al cargar index-business-data:', error));
})();

// Nueva función para cargar empresa y reservas
async function cargarEmpresaYReservas() {
    try {
        const usuarioId = localStorage.getItem('usuario_id');
        if (!usuarioId) {
            console.warn('Usuario no autenticado');
            return;
        }

        // Cargar información de empresa desde BD
        await cargarInfoEmpresa(usuarioId);

        // Cargar reservas recientes desde Firestore
        await loadReservasEspacios();
    } catch (error) {
        console.error('Error cargando datos:', error);
    }
}

// Cargar información real de la empresa
async function cargarInfoEmpresa(usuarioId) {
    try {
        const response = await fetch(`http://pil3g3.duckdns.org/api/usuarios/${usuarioId}`);
        if (response.ok) {
            const usuario = await response.json();
            mostrarInfoEmpresa(usuario);
        }
    } catch (error) {
        console.error('Error cargando info empresa:', error);
    }
}

function mostrarInfoEmpresa(usuario) {
    const infoContainer = document.querySelector('[data-info-empresa]') || crearContenedorInfo();

    if (infoContainer) {
        infoContainer.innerHTML = `
            <div style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 8px 20px rgba(0,0,0,0.06);margin-bottom:24px;">
                <h2 style="margin-top:0;color:#333;margin-bottom:18px;">🏢 Información de la Empresa</h2>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;font-size:0.95rem;line-height:1.8;">
                    <div>
                        <p style="margin:0 0 6px 0;color:#666;"><strong>Nombre:</strong></p>
                        <p style="margin:0;color:#00d4ff;font-weight:600;font-size:1.1rem;">${escapeHtml(usuario.empresa_nombre || usuario.nombre || 'Sin nombre')}</p>
                    </div>
                    <div>
                        <p style="margin:0 0 6px 0;color:#666;"><strong>Email:</strong></p>
                        <p style="margin:0;color:#333;">${escapeHtml(usuario.email || 'No especificado')}</p>
                    </div>
                    <div>
                        <p style="margin:0 0 6px 0;color:#666;"><strong>CIF:</strong></p>
                        <p style="margin:0;color:#333;">${escapeHtml(usuario.empresa_cif || 'No especificado')}</p>
                    </div>
                    <div>
                        <p style="margin:0 0 6px 0;color:#666;"><strong>Teléfono:</strong></p>
                        <p style="margin:0;color:#333;">${escapeHtml(usuario.telefono || 'No especificado')}</p>
                    </div>
                    <div style="grid-column:1/-1;">
                        <p style="margin:0 0 6px 0;color:#666;"><strong>Ciudad:</strong></p>
                        <p style="margin:0;color:#333;">${escapeHtml(usuario.ciudad || 'No especificada')}</p>
                    </div>
                </div>
                <p style="margin-top:16px;padding-top:16px;border-top:1px solid #eee;color:#999;font-size:0.9rem;">
                    Desde aquí puedes gestionar tus reservas, ver el estado de tu solicitud y editar tu perfil.
                </p>
            </div>
        `;
    }
}

function crearContenedorInfo() {
    const cardsRoot = document.getElementById('businessSummaryCards');
    if (cardsRoot && !cardsRoot.previousElementSibling?.getAttribute('data-info-empresa')) {
        const container = document.createElement('div');
        container.setAttribute('data-info-empresa', 'true');
        container.style.cssText = 'width:100%;margin-top:30px;';
        cardsRoot.parentElement.insertBefore(container, cardsRoot);
        return container;
    }
    return document.querySelector('[data-info-empresa]');
}

async function loadReservasEspacios() {
    // Cargar reservas de espacios del usuario autenticado
    try {
        const token = localStorage.getItem('auth_token');
        const usuarioId = localStorage.getItem('usuario_id');

        if (!token || !usuarioId) {
            console.warn('Usuario no autenticado');
            mostrarReservasEspacios([]);
            return;
        }

        const response = await fetch(`http://pil3g3.duckdns.org/api/reservas-espacios/usuario/${usuarioId}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const result = await response.json();
            mostrarReservasEspacios(result || []);
        } else {
            console.warn('No se pudieron cargar reservas:', response.status);
            mostrarReservasEspacios([]);
        }
    } catch (error) {
        console.error('Error cargando reservas:', error);
        mostrarReservasEspacios([]);
    }
}

function mostrarReservasEspacios(reservas) {
    // Mostrar reservas de espacios en el panel
    let reservasContainer = document.getElementById('reservasEspaciosContainer');

    if (!reservasContainer) {
        // Crear contenedor si no existe
        const cardsRoot = document.getElementById('businessSummaryCards');
        if (cardsRoot) {
            const container = document.createElement('div');
            container.id = 'reservasEspaciosContainer';
            container.style.cssText = 'width:100%;margin-top:30px;';
            cardsRoot.parentElement.insertBefore(container, cardsRoot.nextElementSibling);
            reservasContainer = container;
        }
    }

    const container = document.getElementById('reservasEspaciosContainer');
    if (!container) return;

    if (!reservas || reservas.length === 0) {
        container.innerHTML = `
            <div style="text-align:center;padding:40px 20px;background:#f8f9fa;border-radius:12px;margin-top:30px;">
                <p style="margin:0 0 16px 0;color:#666;font-size:1.1rem;">📭 No tienes reservas de espacios aún</p>
                <p style="margin:0 0 18px 0;color:#999;font-size:0.95rem;">Reserva un espacio para tu negocio (food truck, puesto, etc.)</p>
                <a href="reserve-space.html" class="btn-primary" style="padding:12px 24px;text-decoration:none;display:inline-block;">Hacer Primera Reserva →</a>

                <div style="margin-top:24px;padding:16px;background:#f0f9ff;border-left:4px solid #00d4ff;border-radius:8px;text-align:left;max-width:500px;margin-left:auto;margin-right:auto;">
                    <p style="margin:0;color:#0369a1;font-weight:600;font-size:0.9rem;">📞 ¿Necesitas ayuda?</p>
                    <p style="margin:8px 0 0 0;color:#0c4a6e;font-size:0.9rem;">Para más información sobre espacios específicos, contacta al:<br><strong style="font-size:1.1rem;color:#00d4ff;">665 24 34 18</strong></p>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <h2 style="margin-top:40px;margin-bottom:20px;color:#333;">📍 Tus Espacios Reservados</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;margin-bottom:24px;">
            ${reservas.map((reserva) => `
                <div style="background:#fff;border-left:4px solid #00d4ff;border-radius:12px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
                    <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:14px;">
                        <div>
                            <h4 style="margin:0 0 6px 0;color:#00d4ff;font-size:1.1rem;">🎪 ${escapeHtml(reserva.nombre_espacio || 'Espacio')}</h4>
                            <span style="font-size:0.85rem;color:#666;">${escapeHtml(reserva.tipo_espacio || 'Sin especificar')}</span>
                        </div>
                        <span style="background:${reserva.estado === 'confirmada' ? '#10b981' : reserva.estado === 'pendiente' ? '#f59e0b' : '#ef4444'};color:white;padding:6px 14px;border-radius:16px;font-size:0.8rem;font-weight:600;">
                            ✓ ${(reserva.estado || 'pendiente').toUpperCase()}
                        </span>
                    </div>

                    <div style="font-size:0.9rem;color:#666;margin:16px 0;line-height:1.7;border-top:1px solid #eee;padding-top:12px;">
                        <p style="margin:6px 0;"><strong>🎵 Evento:</strong> ${escapeHtml(reserva.evento_id || 'No especificado')}</p>
                        <p style="margin:6px 0;"><strong>📏 Tamaño:</strong> ${escapeHtml(reserva.tamaño || 'Estándar')}</p>
                        <p style="margin:6px 0;"><strong>🏢 Negocio:</strong> ${escapeHtml(reserva.nombre_negocio || 'Mi Empresa')}</p>
                        <p style="margin:6px 0;"><strong>💰 Precio:</strong> €${(reserva.precio || 0).toFixed(2)}</p>
                        ${reserva.descripcion ? `<p style="margin:6px 0;"><strong>📝 Notas:</strong> ${escapeHtml(reserva.descripcion)}</p>` : ''}
                        <p style="margin:6px 0;font-size:0.85rem;color:#999;">
                            <strong>📅 Reservado:</strong> ${new Date(reserva.fecha_reserva || Date.now()).toLocaleDateString('es-ES')}
                        </p>
                    </div>

                    <div style="display:flex;gap:8px;margin-top:14px;">
                        <button onclick="verDetalleReserva(${reserva.id})" style="flex:1;padding:10px 12px;background:#00d4ff;color:white;border:none;border-radius:6px;cursor:pointer;font-size:0.9rem;font-weight:600;transition:all 0.3s;">
                            👁️ Ver Detalles
                        </button>
                        ${reserva.estado === 'pendiente' ? `
                            <button onclick="cancelarReserva(${reserva.id})" style="flex:1;padding:10px 12px;background:#ef4444;color:white;border:none;border-radius:6px;cursor:pointer;font-size:0.9rem;font-weight:600;transition:all 0.3s;">
                                ✕ Cancelar
                            </button>
                        ` : ''}
                    </div>
                </div>
            `).join('')}
        </div>

        <div style="padding:16px;background:#f0f9ff;border-left:4px solid #00d4ff;border-radius:8px;margin-top:20px;">
            <p style="margin:0;color:#0369a1;font-weight:600;font-size:0.95rem;">📞 ¿Necesitas hacer cambios en tu reserva?</p>
            <p style="margin:8px 0 0 0;color:#0c4a6e;font-size:0.9rem;">Contacta al <strong style="font-size:1rem;color:#00d4ff;">665 24 34 18</strong> para más información o cambios específicos</p>
        </div>
    `;
}

function verDetalleReserva(reservaId) {
    // Ver detalles completos de una reserva
    alert('📋 Detalles de Reserva #' + reservaId + '\n\nPara más información, contacta al 665 24 34 18');
}

function cancelarReserva(reservaId) {
    // Cancelar una reserva
    if (confirm('¿Estás seguro de que quieres cancelar esta reserva?')) {
        const token = localStorage.getItem('auth_token');
        if (!token) {
            alert('Debes iniciar sesión');
            return;
        }

        fetch('http://pil3g3.duckdns.org/api/reservas-espacios/' + reservaId + '/cancelar', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(result => {
            alert('✅ Reserva cancelada exitosamente');
            loadReservasEspacios();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('❌ Error de conexión');
        });
    }
}

function fillIndexBusiness(data) {
    const navbarInfo = document.getElementById('businessNavbarInfo');
    const heroContent = document.getElementById('businessHeroContent');
    const cardsRoot = document.getElementById('businessSummaryCards');

    // Obtener nombre de empresa del localStorage
    const empresaNombre = localStorage.getItem('empresa_nombre') || localStorage.getItem('userName') || 'Mi Empresa';

    if (navbarInfo) {
        navbarInfo.innerHTML = `
            <div style="color:var(--light-text);font-weight:600;margin-right:16px;">
                Empresa: <span style="color:#00d4ff;">${escapeHtml(empresaNombre)}</span>
            </div>
            <a href="reserve-space.html" class="btn-primary" style="padding:8px 14px;text-decoration:none;">🏪 Reservar Espacio</a>
        `;
    }

    if (heroContent) {
        heroContent.innerHTML = `
            <h1 style="font-size:2.4rem;margin-bottom:12px;color:var(--light-text);">Bienvenido, ${escapeHtml(empresaNombre)}</h1>
            <p style="opacity:0.85;margin-bottom:20px;font-size:1.1rem;color:var(--light-text);">Panel de Control - Gestiona tus Espacios Reservados</p>
            <a href="reserve-space.html" class="btn-primary" style="padding:14px 28px;font-size:1rem;text-decoration:none;display:inline-block;">🎪 Reservar Nuevo Espacio →</a>
        `;
    }

    if (cardsRoot) {
        cardsRoot.innerHTML = (data.cards || []).map((card) => `
            <div style="flex:${escapeHtml(card.flex || '1')};min-width:260px;background:#fff;border-radius:12px;padding:22px;box-shadow:0 8px 20px rgba(0,0,0,0.06);">
                <h3 style="color:#333;margin-top:0;">${escapeHtml(card.title)}</h3>
                ${(card.lines || []).map((line, index) => `<p style="${index >= 2 ? 'margin-top:12px;' : ''}color:#666;">${line}</p>`).join('')}
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
