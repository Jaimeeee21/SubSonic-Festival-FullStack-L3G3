/**
 * public/admin-data.js
 * Gestión de datos para el panel de administración
 */

class AdminAPI {
    constructor() {
        this.API_BASE = 'http://pil3g3.duckdns.org';
        this.adminToken = localStorage.getItem('admin_token');
    }

    /**
     * Login Admin - Verificar credenciales
     * Por ahora: validación simple con emails específicos
     */
    async loginAdmin(email, password) {
        try {
            // Validación simple para demo
            // En producción: enviar credenciales al backend
            const ADMIN_EMAIL = 'admin@subsonic.com';
            const ADMIN_PASSWORD = 'admin123';

            if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
                this.adminToken = 'admin_token_' + Date.now();
                localStorage.setItem('admin_token', this.adminToken);
                localStorage.setItem('admin_email', email);
                return { success: true, email };
            } else {
                return { 
                    success: false, 
                    error: 'Credenciales inválidas. Use:\nEmail: admin@subsonic.com\nContraseña: admin123' 
                };
            }
        } catch (error) {
            console.error('Error en login admin:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Verificar si el admin está autenticado
     */
    isAdminAuthenticated() {
        return !!localStorage.getItem('admin_token');
    }

    /**
     * Obtener email del admin autenticado
     */
    getAdminEmail() {
        return localStorage.getItem('admin_email') || 'Admin';
    }

    /**
     * Logout Admin
     */
    logoutAdmin() {
        localStorage.removeItem('admin_token');
        localStorage.removeItem('admin_email');
        this.adminToken = null;
    }

    /**
     * Obtener todas las empresas
     */
    async getEmpresas() {
        try {
            const response = await fetch(`${this.API_BASE}/api/empresas/firebase/todas`);
            if (!response.ok) throw new Error('Error al obtener empresas');
            
            const data = await response.json();
            return data.empresas || [];
        } catch (error) {
            console.error('Error obteniendo empresas:', error);
            return [];
        }
    }

    /**
     * Obtener todas las reservas de espacios
     */
    async getReservasEspacios() {
        try {
            const response = await fetch(`${this.API_BASE}/api/reservas-espacios/todas/lista`);
            if (!response.ok) throw new Error('Error al obtener reservas');
            
            const data = await response.json();
            return Array.isArray(data) ? data : [];
        } catch (error) {
            console.error('Error obteniendo reservas:', error);
            return [];
        }
    }

    /**
     * Obtener estadísticas del sistema
     */
    async getStats() {
        try {
            const empresas = await this.getEmpresas();
            const reservas = await this.getReservasEspacios();

            return {
                totalEmpresas: empresas.length,
                totalReservas: reservas.length,
                reservasConfirmadas: reservas.filter(r => r.estado === 'confirmada').length,
                reservasPendientes: reservas.filter(r => r.estado === 'pendiente').length,
                totalEspacios: 15, // Dato fijo por ahora
                totalEventos: 5
            };
        } catch (error) {
            console.error('Error obteniendo stats:', error);
            return {
                totalEmpresas: 0,
                totalReservas: 0,
                reservasConfirmadas: 0,
                reservasPendientes: 0,
                totalEspacios: 0,
                totalEventos: 0
            };
        }
    }

    /**
     * Formatear datos de empresa para tabla
     */
    formatEmpresaRow(empresa) {
        return {
            id: empresa.id || '-',
            nombre: empresa.nombre || '-',
            tipo: empresa.tipo_empresa || '-',
            email: empresa.email_contacto || '-',
            telefono: empresa.telefono || '-',
            estado: empresa.estado || 'activa',
            fecha: empresa.fecha_registro ? new Date(empresa.fecha_registro).toLocaleDateString('es-ES') : '-'
        };
    }

    /**
     * Formatear datos de reserva para tabla
     */
    formatReservaRow(reserva) {
        return {
            id: reserva.id || '-',
            empresa: reserva.empresa_nombre || '-',
            evento: reserva.evento_id || '-',
            espacio: reserva.nombre_espacio || '-',
            tipo: reserva.tipo_espacio || '-',
            estado: reserva.estado || 'pendiente',
            fecha: reserva.fecha_reserva ? new Date(reserva.fecha_reserva).toLocaleDateString('es-ES') : '-'
        };
    }
}

// Instancia global
const adminAPI = new AdminAPI();
