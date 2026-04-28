/**
 * public/cookie-manager.js
 * Gestión automática de cookies HTTP y localStorage sincronizados
 */

class CookieManager {
    constructor() {
        this.COOKIE_KEYS = [
            'auth_token',
            'user_empresa_nombre',
            'user_usuario_id',
            'user_empresa_id',
            'user_email',
            'user_nombre'
        ];
        
        // Sincronizar cookies al cargar la página
        window.addEventListener('load', () => this.syncCookiesFromServer());
    }

    /**
     * Obtener el valor de una cookie por nombre
     */
    getCookie(name) {
        const nameEQ = name + "=";
        const cookies = document.cookie.split(';');
        
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.indexOf(nameEQ) === 0) {
                return decodeURIComponent(cookie.substring(nameEQ.length));
            }
        }
        return null;
    }

    /**
     * Obtener todas las cookies como objeto
     */
    getAllCookies() {
        const cookies = {};
        document.cookie.split(';').forEach(cookie => {
            const [name, value] = cookie.split('=');
            if (name && value) {
                cookies[name.trim()] = decodeURIComponent(value);
            }
        });
        return cookies;
    }

    /**
     * Sincronizar cookies HTTP con localStorage
     * Se llama automáticamente al cargar la página
     */
    syncCookiesFromServer() {
        const cookies = this.getAllCookies();
        
        if (cookies['auth_token']) {
            localStorage.setItem('auth_token', cookies['auth_token']);
        }
        
        if (cookies['user_empresa_nombre']) {
            localStorage.setItem('empresa_nombre', cookies['user_empresa_nombre']);
            localStorage.setItem('userName', cookies['user_empresa_nombre']);
        }
        
        if (cookies['user_usuario_id']) {
            localStorage.setItem('usuario_id', cookies['user_usuario_id']);
            localStorage.setItem('userId', cookies['user_usuario_id']);
        }
        
        if (cookies['user_empresa_id']) {
            localStorage.setItem('empresa_id', cookies['user_empresa_id']);
        }
        
        if (cookies['user_email']) {
            localStorage.setItem('email', cookies['user_email']);
            localStorage.setItem('userEmail', cookies['user_email']);
        }
        
        if (cookies['user_nombre']) {
            localStorage.setItem('userName', cookies['user_nombre']);
        }
        
        console.log('✅ Cookies sincronizadas desde servidor');
    }

    /**
     * Obtener token de autenticación (intenta cookie primero, luego localStorage)
     */
    getAuthToken() {
        return this.getCookie('auth_token') || localStorage.getItem('auth_token');
    }

    /**
     * Verificar si el usuario está autenticado
     */
    isAuthenticated() {
        const token = this.getAuthToken();
        const userId = this.getCookie('user_usuario_id') || localStorage.getItem('userId');
        return !!(token && userId);
    }

    /**
     * Obtener datos del usuario autenticado
     */
    getUserData() {
        return {
            token: this.getAuthToken(),
            usuario_id: this.getCookie('user_usuario_id') || localStorage.getItem('userId'),
            empresa_nombre: this.getCookie('user_empresa_nombre') || localStorage.getItem('empresa_nombre'),
            empresa_id: this.getCookie('user_empresa_id') || localStorage.getItem('empresa_id'),
            email: this.getCookie('user_email') || localStorage.getItem('userEmail'),
            nombre: this.getCookie('user_nombre') || localStorage.getItem('userName'),
            is_empresa: !!this.getCookie('user_empresa_nombre')
        };
    }

    /**
     * Limpiar todas las cookies y localStorage (logout)
     */
    clearAuth() {
        // Limpiar localStorage
        const itemsToRemove = [
            'auth_token', 'firebase_token', 'firebase_user',
            'userId', 'usuario_id', 'userName', 'userEmail', 'userPhoto',
            'empresa_nombre', 'empresa_id', 'email', 'isEmpresa',
            'empresa_email_recordada'
        ];
        
        itemsToRemove.forEach(item => localStorage.removeItem(item));
        
        // Limpiar cookies (establecer max_age = 0)
        this.COOKIE_KEYS.forEach(key => {
            document.cookie = `${key}=; max-age=0; path=/`;
        });
        
        console.log('✅ Autenticación limpiada');
    }

    /**
     * Obtener información de persistencia (para debugging)
     */
    getDebugInfo() {
        return {
            cookies: this.getAllCookies(),
            localStorage: {
                auth_token: localStorage.getItem('auth_token'),
                userId: localStorage.getItem('userId'),
                userName: localStorage.getItem('userName'),
                empresa_nombre: localStorage.getItem('empresa_nombre'),
                isEmpresa: localStorage.getItem('isEmpresa')
            }
        };
    }
}

// Instancia global de CookieManager
const cookieManager = new CookieManager();
