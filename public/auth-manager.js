/**
 * app/public/auth-manager.js
 * Gestión de autenticación con Firebase + Google Sign-In
 */

class AuthManager {
  constructor() {
    this.token = localStorage.getItem('firebase_token');
    this.user = JSON.parse(localStorage.getItem('firebase_user') || 'null');
    this.isAuthenticated = !!this.token;
  }

  /**
   * Decodificar JWT de Google (sin verificación, solo para cliente)
   * Maneja correctamente caracteres UTF-8
   */
  decodeGoogleToken(token) {
    try {
      const parts = token.split('.');
      if (parts.length !== 3) throw new Error('Token inválido');
      
      // Decodificación correcta de Base64 URL-safe con soporte UTF-8
      let payload = parts[1];
      // Agregar padding si es necesario
      const padding = 4 - (payload.length % 4);
      if (padding !== 4) {
        payload += '='.repeat(padding);
      }
      
      // Decodificar Base64 a string con soporte UTF-8
      const binaryString = atob(payload);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      const decoder = new TextDecoder('utf-8');
      const decodedString = decoder.decode(bytes);
      
      const decoded = JSON.parse(decodedString);
      return decoded;
    } catch (error) {
      console.error('Error decodificando token:', error);
      return null;
    }
  }

  /**
   * Login con Google
   */
  async loginWithGoogle(googleToken) {
    try {
      // Enviar token de Google al backend para verificarlo
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: googleToken })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en autenticación');
      }

      const data = await response.json();
      
      // Decodificar el token de Google para obtener la información del usuario
      const tokenInfo = this.decodeGoogleToken(googleToken);
      
      // Guardar token y usuario
      this.token = googleToken;
      this.user = {
        uid: data.user_id,
        email: tokenInfo?.email || 'email@example.com',
        displayName: tokenInfo?.name || 'Usuario',
        picture: tokenInfo?.picture || null
      };

      localStorage.setItem('firebase_token', googleToken);
      localStorage.setItem('firebase_user', JSON.stringify(this.user));
      localStorage.setItem('userId', data.user_id); // Guardar userId para profile.html
      localStorage.setItem('userName', this.user.displayName); // Guardar userName para navbar
      localStorage.setItem('userEmail', this.user.email); // Guardar email
      localStorage.setItem('userPhoto', this.user.picture || ''); // Guardar foto de perfil

      this.isAuthenticated = true;
      console.log('✅ Autenticación exitosa:', this.user);
      
      return { success: true, user: this.user };
    } catch (error) {
      console.error('❌ Error en login:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Registrar nuevo usuario con email
   */
  async register(email, password, name) {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          email, 
          password, 
          name
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en registro');
      }

      const data = await response.json();
      
      // Generar un token JWT simple para el frontend
      const fakeToken = btoa(JSON.stringify({ 
        email, 
        name,
        sub: data.user_id,
        iat: Math.floor(Date.now() / 1000)
      }));
      
      // Guardar token y usuario
      this.token = fakeToken;
      this.user = {
        uid: data.user_id,
        email: email,
        displayName: name,
        picture: null
      };

      localStorage.setItem('firebase_token', fakeToken);
      localStorage.setItem('firebase_user', JSON.stringify(this.user));
      localStorage.setItem('userId', data.user_id); // Guardar userId para profile.html
      localStorage.setItem('userName', this.user.displayName); // Guardar userName para navbar
      localStorage.setItem('userEmail', this.user.email); // Guardar email
      localStorage.setItem('userPhoto', ''); // Sin foto en registro

      this.isAuthenticated = true;
      console.log('✅ Registro exitoso:', this.user);
      
      return { success: true, user: this.user };
    } catch (error) {
      console.error('❌ Error en registro:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Login con email y contraseña para CLIENTES
   */
  async loginEmail(email, password) {
    try {
      const response = await fetch('/api/auth/login-email-client', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en autenticación');
      }

      const data = await response.json();

      // Generar un token JWT simple para el frontend
      const fakeToken = btoa(JSON.stringify({
        email,
        sub: data.user_id,
        iat: Math.floor(Date.now() / 1000)
      }));

      // Guardar token y usuario
      this.token = fakeToken;
      this.user = {
        uid: data.user_id,
        email: email,
        displayName: email.split('@')[0],
        picture: null
      };

      localStorage.setItem('firebase_token', fakeToken);
      localStorage.setItem('firebase_user', JSON.stringify(this.user));
      localStorage.setItem('userId', data.user_id); // Guardar userId para profile.html
      localStorage.setItem('userName', this.user.displayName); // Guardar userName para navbar
      localStorage.setItem('userEmail', this.user.email); // Guardar email
      localStorage.setItem('userPhoto', ''); // Sin foto en login email

      this.isAuthenticated = true;
      console.log('✅ Login exitoso:', this.user);

      return { success: true, user: this.user };
    } catch (error) {
      console.error('❌ Error en login:', error);
      return { success: false, error: error.message };
    }
  }

  
  logout() {
    localStorage.removeItem('firebase_token');
    localStorage.removeItem('firebase_user');
    this.token = null;
    this.user = null;
    this.isAuthenticated = false;
    console.log('✅ Sesión cerrada');
  }

  /**
   * Obtener token actual
   */
  getToken() {
    return this.token;
  }

  /**
   * Obtener usuario actual
   */
  getUser() {
    return this.user;
  }

  /**
   * Verificar si está autenticado
   */
  isLoggedIn() {
    return this.isAuthenticated;
  }

  /**
   * Obtener headers con autorización
   */
  getAuthHeaders() {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    };
  }

  /**
   * Hacer request autenticado al backend
   */
  async fetchWithAuth(url, options = {}) {
    if (!this.token) {
      throw new Error('No hay token de autenticación');
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers
      }
    });

    if (response.status === 401) {
      this.logout();
      throw new Error('Token expirado, inicie sesión nuevamente');
    }

    return response;
  }
}

// Crear instancia global
window.authManager = new AuthManager();
