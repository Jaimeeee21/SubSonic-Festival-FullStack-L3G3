/**
 * public/admin-view.js
 * Renderización del panel de administración
 */

// Verificar autenticación al cargar
document.addEventListener('DOMContentLoaded', async () => {
    if (adminAPI.isAdminAuthenticated()) {
        await loadAdminDashboard();
    } else {
        showAdminLogin();
    }
});

/**
 * Mostrar vista de login
 */
function showAdminLogin() {
    document.getElementById('adminLoginView').style.display = 'block';
    document.getElementById('adminDashboard').style.display = 'none';

    const form = document.getElementById('adminLoginForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('adminEmail').value;
        const password = document.getElementById('adminPassword').value;
        const errorDiv = document.getElementById('adminLoginError');

        const result = await adminAPI.loginAdmin(email, password);

        if (result.success) {
            errorDiv.innerHTML = '';
            await loadAdminDashboard();
        } else {
            errorDiv.innerHTML = `<div class="error-message">${result.error}</div>`;
        }
    });
}

/**
 * Mostrar dashboard admin
 */
async function loadAdminDashboard() {
    document.getElementById('adminLoginView').style.display = 'none';
    document.getElementById('adminDashboard').style.display = 'block';
    document.getElementById('adminUsername').textContent = adminAPI.getAdminEmail();

    // Cargar datos
    await loadStats();
    await loadEmpresas();
    await loadReservas();
    
    // Actualizar última actualización
    const now = new Date();
    document.getElementById('lastUpdate').textContent = now.toLocaleString('es-ES');
}

/**
 * Cargar y mostrar estadísticas
 */
async function loadStats() {
    const stats = await adminAPI.getStats();

    document.getElementById('totalEmpresas').textContent = stats.totalEmpresas;
    document.getElementById('totalReservas').textContent = stats.totalReservas;
    document.getElementById('totalEspacios').textContent = stats.totalEspacios;
    document.getElementById('totalEventos').textContent = stats.totalEventos;
}

/**
 * Cargar y mostrar empresas registradas
 */
async function loadEmpresas() {
    const container = document.getElementById('empresasContent');
    const loading = document.getElementById('empresasLoading');

    try {
        const empresas = await adminAPI.getEmpresas();
        loading.style.display = 'none';

        if (empresas.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>No hay empresas registradas aún</p>
                </div>
            `;
            return;
        }

        let html = `
            <div class="table-responsive">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Tipo</th>
                            <th>Email</th>
                            <th>Teléfono</th>
                            <th>Estado</th>
                            <th>Fecha Registro</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        empresas.forEach(empresa => {
            const row = adminAPI.formatEmpresaRow(empresa);
            const estadoBadge = row.estado === 'activa' 
                ? '<span class="badge badge-success">Activa</span>'
                : '<span class="badge badge-pending">Inactiva</span>';

            html += `
                <tr>
                    <td><strong>${row.nombre}</strong></td>
                    <td>${row.tipo}</td>
                    <td>${row.email}</td>
                    <td>${row.telefono}</td>
                    <td>${estadoBadge}</td>
                    <td>${row.fecha}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        container.innerHTML = html;
    } catch (error) {
        console.error('Error cargando empresas:', error);
        loading.style.display = 'none';
        container.innerHTML = `
            <div class="error-message">Error cargando empresas: ${error.message}</div>
        `;
    }
}

/**
 * Cargar y mostrar reservas
 */
async function loadReservas() {
    const container = document.getElementById('reservasContent');
    const loading = document.getElementById('reservasLoading');

    try {
        const reservas = await adminAPI.getReservasEspacios();
        loading.style.display = 'none';

        if (reservas.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-calendar"></i>
                    <p>No hay reservas registradas aún</p>
                </div>
            `;
            return;
        }

        let html = `
            <div class="table-responsive">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Empresa</th>
                            <th>Evento</th>
                            <th>Espacio</th>
                            <th>Tipo</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        reservas.forEach(reserva => {
            const row = adminAPI.formatReservaRow(reserva);
            let estadoBadge = '<span class="badge badge-pending">Pendiente</span>';
            
            if (row.estado === 'confirmada') {
                estadoBadge = '<span class="badge badge-success">Confirmada</span>';
            } else if (row.estado === 'rechazada') {
                estadoBadge = '<span class="badge" style="background: #fee; color: #c33;">Rechazada</span>';
            } else if (row.estado === 'cancelada') {
                estadoBadge = '<span class="badge badge-pending">Cancelada</span>';
            }

            html += `
                <tr>
                    <td><small>${row.id.substring(0, 8)}...</small></td>
                    <td><strong>${row.empresa}</strong></td>
                    <td>${row.evento}</td>
                    <td>${row.espacio}</td>
                    <td>${row.tipo}</td>
                    <td>${estadoBadge}</td>
                    <td>${row.fecha}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        container.innerHTML = html;
    } catch (error) {
        console.error('Error cargando reservas:', error);
        loading.style.display = 'none';
        container.innerHTML = `
            <div class="error-message">Error cargando reservas: ${error.message}</div>
        `;
    }
}

/**
 * Logout del admin
 */
function adminLogout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        adminAPI.logoutAdmin();
        location.reload();
    }
}
