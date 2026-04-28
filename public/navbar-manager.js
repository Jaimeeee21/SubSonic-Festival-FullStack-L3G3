/**
 * navbar-manager.js - Gestiona la navbar y sesión en todas las páginas
 * Mantiene la persistencia de sesión globalmente
 */

class NavbarManager {
    constructor() {
        console.log('🎨 [NavbarManager] Inicializando...');
        this.updateNavbar();
        this.attachEventListeners();
    }

    /**
     * Actualizar la navbar basado en el estado de autenticación
     */
    updateNavbar() {
        try {
            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            const userName = localStorage.getItem('userName') || sessionStorage.getItem('userName') || 'Usuario';
            const userPhoto = localStorage.getItem('userPhoto') || sessionStorage.getItem('userPhoto');
            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            const isProfilePage = currentPage === 'profile.html';
            
            console.log('[NavbarManager] Pagina actual:', currentPage);
            
            const navRight = document.querySelector('.nav-right');
            
            if (!navRight) {
                console.warn('[NavbarManager] No se encontro .nav-right');
                return;
            }

            if (userId) {
                // Usuario autenticado
                console.log('[NavbarManager] Usuario autenticado:', userId);
                
                // Sanitizar nombre para evitar problemas con caracteres especiales
                const displayName = String(userName).substring(0, 20); // Limitar a 20 caracteres
                
                // Buscar o crear contenedor de usuario
                let userContainer = document.getElementById('userMenuContainer');
                if (!userContainer) {
                    userContainer = document.createElement('div');
                    userContainer.id = 'userMenuContainer';
                    // Insertar al principio, antes del cartBtn si existe
                    const cartBtn = navRight.querySelector('#cartBtn');
                    if (cartBtn) {
                        cartBtn.parentNode.insertBefore(userContainer, cartBtn);
                    } else {
                        navRight.insertBefore(userContainer, navRight.firstChild);
                    }
                }
                
                let navHtml = `
                    <span style="color: #00f0ff; font-weight: 500; cursor: pointer; max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" id="userNameNav" title="Click para ir a perfil">${displayName}</span>
                `;
                
                // Solo agregar boton logout en profile.html
                if (isProfilePage) {
                    navHtml += `
                        <button id="logoutBtnNav" class="logout-btn-nav" style="
                            background: #ff006e;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-weight: 500;
                            margin-left: 10px;
                        ">Logout</button>
                    `;
                }
                
                userContainer.innerHTML = navHtml;
                userContainer.style.display = 'flex';
                userContainer.style.alignItems = 'center';
                userContainer.style.gap = '10px';

                // Ocultar el link "Sesion" si existe
                const userIcon = navRight.querySelector('a.user-icon');
                if (userIcon) {
                    userIcon.style.display = 'none';
                }

                // Adjuntar eventos
                const userNameElement = document.getElementById('userNameNav');
                if (userNameElement) {
                    userNameElement.addEventListener('click', () => window.location.href = 'profile.html');
                }

                const logoutBtn = document.getElementById('logoutBtnNav');
                if (logoutBtn) {
                    logoutBtn.addEventListener('click', () => this.handleLogout());
                }
            } else {
                // Usuario no autenticado - eliminar contenedor si existe
                const userContainer = document.getElementById('userMenuContainer');
                if (userContainer) {
                    userContainer.remove();
                }
                
                // Mostrar el link "Sesion"
                const userIcon = navRight.querySelector('a.user-icon');
                if (userIcon) {
                    userIcon.style.display = 'inline';
                }
            }
        } catch (error) {
            console.error('[NavbarManager] Error actualizando navbar:', error);
        }
    }

    /**
     * Adjuntar event listeners generales
     */
    attachEventListeners() {
        // Escuchar cambios en localStorage desde otras pestañas
        window.addEventListener('storage', (e) => {
            if (e.key === 'userId' || e.key === 'userName' || e.key === 'userPhoto') {
                console.log('[NavbarManager] Cambio detectado en localStorage desde otra pestaña');
                this.updateNavbar();
            }
        });
    }

    /**
     * Manejar logout
     */
    handleLogout() {
        if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
            console.log('🚪 [NavbarManager] Logout ejecutado');
            localStorage.removeItem('userId');
            localStorage.removeItem('userName');
            localStorage.removeItem('userPhoto');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('firebase_token');
            localStorage.removeItem('firebase_user');
            sessionStorage.removeItem('userId');
            sessionStorage.removeItem('userName');
            sessionStorage.removeItem('userPhoto');
            sessionStorage.removeItem('userEmail');
            
            // Redirigir a login
            window.location.href = 'login.html';
        }
    }

    /**
     * Obtener userId actual
     */
    getCurrentUserId() {
        return localStorage.getItem('userId') || sessionStorage.getItem('userId');
    }

    /**
     * Verificar si está autenticado
     */
    isAuthenticated() {
        return !!this.getCurrentUserId();
    }
}

// Inicializar cuando el documento esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.navbarManager = new NavbarManager();
        console.log('[navbar-manager] Cargado correctamente');
    });
} else {
    window.navbarManager = new NavbarManager();
    console.log('[navbar-manager] Cargado correctamente');
}
