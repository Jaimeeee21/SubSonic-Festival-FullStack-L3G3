/**
 * profile-view.js - Gestiona la interfaz de usuario del perfil
 */

class ProfileView {
    constructor() {
        this.initElements();
        this.attachEventListeners();
    }

    /**
     * Inicializar referencias a elementos del DOM
     */
    initElements() {
        // Elementos de perfil
        this.profilePhoto = document.getElementById('profilePhoto');
        this.changePhotoBtn = document.getElementById('changePhotoBtn');
        this.photoInput = document.getElementById('photoInput');
        
        this.userName = document.getElementById('userName');
        this.userEmail = document.getElementById('userEmail');
        this.userPhone = document.getElementById('userPhone');
        this.userCity = document.getElementById('userCity');
        this.userDate = document.getElementById('userDate');
        this.userType = document.getElementById('userType');
        this.userBio = document.getElementById('userBio');

        // Botones
        this.editProfileBtn = document.getElementById('editProfileBtn');

        // Modal de edición
        this.editProfileModal = document.getElementById('editProfileModal');
        this.editProfileForm = document.getElementById('editProfileForm');
        this.closeModalBtn = this.editProfileModal.querySelector('.close');
        this.cancelEditBtn = document.getElementById('cancelEditBtn');

        // Campos del formulario de edición
        this.editName = document.getElementById('editName');
        this.editEmail = document.getElementById('editEmail');
        this.editPhone = document.getElementById('editPhone');
        this.editCity = document.getElementById('editCity');
        this.editBio = document.getElementById('editBio');

        // Contenedor de entradas
        this.ticketsContainer = document.getElementById('ticketsContainer');
        this.noTicketsMessage = document.getElementById('noTicketsMessage');
    }

    /**
     * Adjuntar event listeners
     */
    attachEventListeners() {
        // Foto de perfil - DESACTIVADO
        // this.changePhotoBtn.addEventListener('click', () => this.photoInput.click());
        // this.photoInput.addEventListener('change', (e) => this.handlePhotoChange(e));

        // Editar perfil
        this.editProfileBtn.addEventListener('click', () => this.openEditModal());
        this.closeModalBtn.addEventListener('click', () => this.closeEditModal());
        this.cancelEditBtn.addEventListener('click', () => this.closeEditModal());
        this.editProfileForm.addEventListener('submit', (e) => this.handleProfileUpdate(e));

        // Cerrar modal al hacer clic fuera
        window.addEventListener('click', (event) => {
            if (event.target == this.editProfileModal) {
                this.closeEditModal();
            }
        });
    }

    /**
     * Cargar y mostrar los datos del perfil
     */
    async loadAndDisplayProfile() {
        try {
            console.log('[loadAndDisplayProfile] Iniciando carga de perfil');
            
            // Verificar autenticación
            const isAuthenticated = profileDataManager.isAuthenticated();
            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            
            console.log('[loadAndDisplayProfile] isAuthenticated:', isAuthenticated, 'userId:', userId);
            
            if (!isAuthenticated) {
                console.error('[loadAndDisplayProfile] Usuario no autenticado');
                this.showError('Por favor, inicia sesión para ver tu perfil.');
                return;
            }

            // Mostrar spinner de carga
            this.showLoading();
            console.log('[loadAndDisplayProfile] Mostrando loading spinner');

            // Cargar datos del perfil
            console.log('[loadAndDisplayProfile] Llamando a loadUserProfile()');
            const profileData = await profileDataManager.loadUserProfile();
            
            console.log('[loadAndDisplayProfile] Datos cargados:', profileData);
            
            // Mostrar información del usuario
            this.displayUserInfo(profileData.usuario);
            
            // Mostrar entradas
            this.displayTickets(profileData.entradas);

            this.hideLoading();
            console.log('[loadAndDisplayProfile] Perfil cargado exitosamente');
        } catch (error) {
            console.error('[loadAndDisplayProfile] Error:', error);
            this.showError(`Error al cargar el perfil: ${error.message}`);
            this.hideLoading();
        }
    }

    /**
     * Mostrar información del usuario
     */
    displayUserInfo(user) {
        if (!user) return;

        // Actualizar foto de perfil - DESACTIVADO
        // if (user.foto_perfil) {
        //     this.profilePhoto.src = user.foto_perfil;
        //     // Guardar en localStorage para que aparezca en navbar
        //     localStorage.setItem('userPhoto', user.foto_perfil);
        // }

        // Actualizar información
        this.userName.textContent = user.nombre || 'Usuario';
        this.userEmail.textContent = user.email || 'email@example.com';
        this.userPhone.textContent = user.telefono || 'No especificado';
        this.userCity.textContent = user.ciudad || 'No especificado';
        this.userDate.textContent = profileDataManager.formatDate(user.created_at || user.fecha_creacion);
        this.userType.textContent = user.es_empresa ? 'Empresa' : 'Usuario Individual';
        this.userBio.textContent = user.bio || 'Sin información adicional';

        // Actualizar formulario de edición
        this.editName.value = user.nombre || '';
        this.editEmail.value = user.email || '';
        this.editPhone.value = user.telefono || '';
        this.editCity.value = user.ciudad || '';
        this.editBio.value = user.bio || '';
        
        // Notificar a navbar-manager que actualice la navbar
        if (window.navbarManager) {
            console.log('[displayUserInfo] Actualizando navbar con nueva foto');
            window.navbarManager.updateNavbar();
        }
    }

    /**
     * Mostrar entradas compradas
     */
    async displayTickets(tickets) {
        if (!tickets || tickets.length === 0) {
            this.ticketsContainer.innerHTML = '';
            this.ticketsContainer.style.display = 'none';
            this.noTicketsMessage.style.display = 'flex';
            return;
        }

        try {
            if (!window.EVENTOS_DATA) {
                const res = await fetch('eventos-data.json');
                window.EVENTOS_DATA = await res.json();
            }
        } catch (e) {
            console.error("Error al cargar eventos en perfil", e);
        }

        this.noTicketsMessage.style.display = 'none';
        this.ticketsContainer.style.display = 'grid';
        this.ticketsContainer.innerHTML = '';

        tickets.forEach(ticket => {
            const ticketCard = this.createTicketCard(ticket);
            this.ticketsContainer.appendChild(ticketCard);
        });
    }

    /**
     * Crear tarjeta de entrada
     */
    createTicketCard(ticket) {
        const card = document.createElement('div');
        card.className = 'ticket-card';

        const estado = ticket.estado || 'confirmada';
        const estadoClase = `estado-${estado.toLowerCase()}`;

        // Intentar obtener fecha real del evento
        let fechaReal = ticket.fecha_evento || ticket.date;
        if (!fechaReal && window.EVENTOS_DATA && window.EVENTOS_DATA.principales) {
            const evRef = window.EVENTOS_DATA.principales.find(e => 
                (ticket.evento_id && ticket.evento_id.includes(e.id)) || 
                (ticket.evento_ciudad && e.location.includes(ticket.evento_ciudad))
            );
            if (evRef) fechaReal = evRef.date;
        }

        const fechaEvento = fechaReal || profileDataManager.formatDate(ticket.fecha_compra || '');
        const precio = profileDataManager.formatCurrency(ticket.precio_total || 0);

        card.innerHTML = `
            <div class="ticket-header">
                <h3>${ticket.evento_nombre || ticket.evento_id || 'Evento'} - ${ticket.evento_ciudad || 'Ciudad no especificada'}</h3>
                <span class="ticket-status ${estadoClase}">${estado.toUpperCase()}</span>
            </div>
            <div class="ticket-body">
                <div class="ticket-info">
                    <div class="info-item">
                        <i class="fas fa-ticket-alt"></i>
                        <span>${ticket.tipo_entrada || 'Entrada Genérica'}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-calendar"></i>
                        <span>${fechaEvento}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-users"></i>
                        <span>${ticket.cantidad_entradas || 1} entrada(s)</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-money-bill"></i>
                        <span>${precio}</span>
                    </div>
                </div>
                <p class="ticket-id">Ref: ${ticket.id || 'N/A'}</p>
            </div>
            <div class="ticket-footer">
                <button class="btn-small btn-view" data-ticket-id="${ticket.id}">
                    <i class="fas fa-eye"></i> Detalles
                </button>
            </div>
        `;

        // Agregar event listeners a los botones
        const viewBtn = card.querySelector('.btn-view');

        viewBtn.addEventListener('click', () => this.handleViewTicketDetails(ticket));

        return card;
    }

    /**
     * Manejar cambio de foto de perfil
     */
    async handlePhotoChange(event) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            this.showLoading();

            // Procesar y subir foto
            const photoDataUrl = await profileDataManager.processPhotoUpload(file);
            
            // Actualizar la vista
            this.profilePhoto.src = photoDataUrl;

            this.showSuccess('Foto de perfil actualizada correctamente');
            this.hideLoading();
        } catch (error) {
            console.error('Error uploading photo:', error);
            this.showError(`Error al subir la foto: ${error.message}`);
            this.hideLoading();
        }

        // Limpiar el input
        event.target.value = '';
    }

    /**
     * Abrir modal de edición
     */
    openEditModal() {
        this.editProfileModal.style.display = 'block';
    }

    /**
     * Cerrar modal de edición
     */
    closeEditModal() {
        this.editProfileModal.style.display = 'none';
    }

    /**
     * Manejar actualización del perfil
     */
    async handleProfileUpdate(event) {
        event.preventDefault();

        try {
            this.showLoading();

            const updatedData = {
                nombre: this.editName.value,
                email: this.editEmail.value,
                telefono: this.editPhone.value,
                ciudad: this.editCity.value,
                bio: this.editBio.value
            };

            await profileDataManager.updateProfile(updatedData);

            // Actualizar la vista
            this.displayUserInfo(profileDataManager.currentUser);
            this.closeEditModal();
            this.showSuccess('Perfil actualizado correctamente');
            this.hideLoading();
        } catch (error) {
            console.error('Error updating profile:', error);
            this.showError(`Error al actualizar el perfil: ${error.message}`);
            this.hideLoading();
        }
    }

    /**
     * Manejar vista de detalles de entrada
     */
    handleViewTicketDetails(ticket) {
        let fechaReal = ticket.fecha_evento || ticket.date;
        if (!fechaReal && window.EVENTOS_DATA && window.EVENTOS_DATA.principales) {
            const evRef = window.EVENTOS_DATA.principales.find(e => 
                (ticket.evento_id && ticket.evento_id.includes(e.id)) || 
                (ticket.evento_ciudad && e.location.includes(ticket.evento_ciudad))
            );
            if (evRef) fechaReal = evRef.date;
        }

        const fechaEventoTexto = fechaReal || profileDataManager.formatDate(ticket.fecha_compra || '');

        // Crear un modal o ir a una página de detalles
        const details = `
            Evento: ${ticket.evento_nombre || ticket.evento_id} - ${ticket.evento_ciudad || ''}
            Fecha del Evento: ${fechaEventoTexto}
            Entrada: ${ticket.tipo_entrada || ticket.id || 'N/A'}
            Cantidad: ${ticket.cantidad_entradas}
            Precio: ${profileDataManager.formatCurrency(ticket.precio_total || 0)}
            Estado: ${ticket.estado || 'confirmada'}
        `;

        alert(details);
    }

    /**
     * Mostrar mensaje de carga
     */
    showLoading() {
        // Agregar clase de carga al body
        document.body.classList.add('loading');
    }

    /**
     * Ocultar mensaje de carga
     */
    hideLoading() {
        document.body.classList.remove('loading');
    }

    /**
     * Mostrar mensaje de éxito
     */
    showSuccess(message) {
        const notification = this.createNotification(message, 'success');
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    /**
     * Mostrar mensaje de error
     */
    showError(message) {
        const notification = this.createNotification(message, 'error');
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

    /**
     * Crear elemento de notificación
     */
    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        return notification;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 [profile-view.js DOMContentLoaded] DOM listo, esperando profileDataManager...');
    
    // Esperar a que profileDataManager esté disponible (máximo 3 segundos)
    let attempts = 0;
    const checkInterval = setInterval(() => {
        attempts++;
        console.log(`🔍 [profile-view.js] Intento ${attempts}: ¿profileDataManager disponible?`, typeof profileDataManager !== 'undefined');
        
        if (typeof profileDataManager !== 'undefined') {
            clearInterval(checkInterval);
            console.log('✅ profileDataManager cargado, inicializando ProfileView');
            try {
                const profileView = new ProfileView();
                profileView.loadAndDisplayProfile();
            } catch (error) {
                console.error('❌ Error al inicializar ProfileView:', error);
            }
            return;
        }
        
        if (attempts > 30) { // 30 * 100ms = 3 segundos
            clearInterval(checkInterval);
            console.error('❌ profileDataManager no se cargó después de 3 segundos');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'notification notification-error';
            errorDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999;';
            errorDiv.innerHTML = `
                <div class="notification-content" style="display: flex; align-items: center; gap: 10px; background: #ff006e; color: white; padding: 15px 20px; border-radius: 5px;">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>Error al cargar el perfil: Recurso no disponible. Recarga la página.</span>
                </div>
            `;
            document.body.appendChild(errorDiv);
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }, 100);
});
