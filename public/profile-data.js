/**
 * profile-data.js - Gestiona la lógica de datos para el perfil del usuario
 * Comunicación con la API backend
 */

class ProfileDataManager {
    constructor() {
        this.apiBaseUrl = window.API_BASE_URL || 'http://pil3g3.duckdns.org/api';
        this.currentUserId = this.getUserIdFromStorage();
        this.currentUser = null;
        this.userTickets = [];
    }

    /**
     * Obtener el ID del usuario del localStorage o sessionStorage
     */
    getUserIdFromStorage() {
        return localStorage.getItem('userId') || sessionStorage.getItem('userId');
    }

    /**
     * Verificar si el usuario está autenticado
     * Verifica directamente en localStorage para evitar issues de timing
     */
    isAuthenticated() {
        const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
        return !!userId;
    }

    /**
     * Cargar el perfil completo del usuario incluyendo entradas
     */
    async loadUserProfile() {
        try {
            console.log('[loadUserProfile] Iniciando carga de perfil');
            
            if (!this.isAuthenticated()) {
                console.error('[loadUserProfile] Usuario no autenticado');
                throw new Error('Usuario no autenticado');
            }

            // Obtener userId nuevamente para asegurar que está actualizado
            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            console.log('[loadUserProfile] userId:', userId);
            
            const url = `${this.apiBaseUrl}/usuarios/${userId}/perfil`;
            console.log('[loadUserProfile] URL:', url);
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            console.log('[loadUserProfile] Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('[loadUserProfile] Error response:', errorText);
                throw new Error(`Error al cargar el perfil: ${response.status} ${errorText}`);
            }

            const data = await response.json();
            console.log('[loadUserProfile] Datos recibidos:', data);
            
            this.currentUser = data.usuario || data;
            
            // Combinar las entradas de ambos posibles sitios (Firestore arrays vs SQLite/Firestore collections)
            let tickets = data.entradas || [];
            if (this.currentUser && this.currentUser.entradas_compradas) {
                // Combinar sin duplicados - o simplemente usar entradas_compradas si tickets está vacío
                if (tickets.length === 0) {
                    tickets = this.currentUser.entradas_compradas;
                } else {
                    tickets = [...tickets, ...this.currentUser.entradas_compradas];
                }
            }
            this.userTickets = tickets;

            return {
                usuario: this.currentUser,
                entradas: this.userTickets
            };
        } catch (error) {
            console.error('❌ [loadUserProfile] Error:', error);
            throw error;
        }
    }

    /**
     * Obtener solo la información del usuario
     */
    async getUser() {
        try {
            if (!this.isAuthenticated()) {
                throw new Error('Usuario no autenticado');
            }

            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            const response = await fetch(`${this.apiBaseUrl}/usuarios/${userId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error al obtener usuario: ${response.status}`);
            }

            const user = await response.json();
            this.currentUser = user;
            return user;
        } catch (error) {
            console.error('Error getting user:', error);
            throw error;
        }
    }

    /**
     * Obtener las entradas compradas del usuario
     */
    async getUserTickets() {
        try {
            if (!this.isAuthenticated()) {
                throw new Error('Usuario no autenticado');
            }

            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');

            // Endpoint para obtener reservas del usuario
            const response = await fetch(`${this.apiBaseUrl}/reservas/usuario/${userId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error al obtener entradas: ${response.status}`);
            }

            const tickets = await response.json();
            this.userTickets = Array.isArray(tickets) ? tickets : [];
            return this.userTickets;
        } catch (error) {
            console.error('Error getting tickets:', error);
            // Si el endpoint no existe, retornar array vacío
            this.userTickets = [];
            return this.userTickets;
        }
    }

    /**
     * Actualizar la foto de perfil del usuario
     */
    async updateProfilePhoto(photoDataUrl) {
        try {
            if (!this.isAuthenticated()) {
                throw new Error('Usuario no autenticado');
            }

            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');

            const response = await fetch(`${this.apiBaseUrl}/usuarios/${userId}/foto-perfil`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    foto_perfil: photoDataUrl
                })
            });

            if (!response.ok) {
                throw new Error(`Error al actualizar foto: ${response.status}`);
            }

            const updatedUser = await response.json();
            this.currentUser = updatedUser;
            return updatedUser;
        } catch (error) {
            console.error('Error updating profile photo:', error);
            throw error;
        }
    }

    /**
     * Actualizar información del perfil del usuario
     */
    async updateProfile(profileData) {
        try {
            if (!this.isAuthenticated()) {
                throw new Error('Usuario no autenticado');
            }

            // Filtrar solo campos que sean permitidos para actualizar
            const allowedFields = ['nombre', 'email', 'telefono', 'ciudad', 'bio'];
            const updateData = {};
            
            for (const field of allowedFields) {
                if (field in profileData) {
                    updateData[field] = profileData[field];
                }
            }

            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');

            const response = await fetch(`${this.apiBaseUrl}/usuarios/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updateData)
            });

            if (!response.ok) {
                throw new Error(`Error al actualizar perfil: ${response.status}`);
            }

            const updatedUser = await response.json();
            this.currentUser = updatedUser;
            return updatedUser;
        } catch (error) {
            console.error('Error updating profile:', error);
            throw error;
        }
    }

    /**
     * Convertir imagen a Base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
    }

    /**
     * Procesar foto seleccionada
     */
    async processPhotoUpload(file) {
        try {
            if (!file.type.startsWith('image/')) {
                throw new Error('El archivo debe ser una imagen');
            }

            if (file.size > 5 * 1024 * 1024) { // 5MB límite
                throw new Error('La imagen es demasiado grande (máximo 5MB)');
            }

            const base64Photo = await this.fileToBase64(file);
            await this.updateProfilePhoto(base64Photo);
            
            return base64Photo;
        } catch (error) {
            console.error('Error processing photo upload:', error);
            throw error;
        }
    }

    /**
     * Obtener detalles de una entrada/reserva
     */
    async getTicketDetails(ticketId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/reservas/${ticketId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error al obtener detalles de entrada: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting ticket details:', error);
            throw error;
        }
    }

    /**
     * Obtener detalles del evento de una reserva
     */
    async getEventDetails(eventoId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/eventos/${eventoId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error al obtener evento: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting event details:', error);
            return null;
        }
    }

    /**
     * Descargar/Imprimir entrada
     */
    downloadTicket(ticketId) {
        try {
            // Generar PDF o descargar ticket
            window.open(`${this.apiBaseUrl}/reservas/${ticketId}/descargar`, '_blank');
        } catch (error) {
            console.error('Error downloading ticket:', error);
            throw error;
        }
    }

    /**
     * Logout del usuario
     */
    logout() {
        localStorage.removeItem('userId');
        localStorage.removeItem('userToken');
        sessionStorage.removeItem('userId');
        sessionStorage.removeItem('userToken');
        window.location.href = 'login.html';
    }

    /**
     * Formatear fecha
     */
    formatDate(dateString) {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch (error) {
            return dateString;
        }
    }

    /**
     * Formatear moneda
     */
    formatCurrency(amount) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'EUR'
        }).format(amount);
    }

    /**
     * Guardar una entrada comprada para el usuario
     */
    async saveTicketPurchase(entrada) {
        try {
            if (!this.isAuthenticated()) {
                throw new Error('Usuario no autenticado');
            }

            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            const url = `${this.apiBaseUrl}/usuarios/${userId}/entradas-compradas`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(entrada)
            });

            if (!response.ok) {
                throw new Error(`Error al guardar entrada: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error saving ticket purchase:', error);
            throw error;
        }
    }
}

// Crear instancia global
const profileDataManager = new ProfileDataManager();
