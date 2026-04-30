/**
 * purchase-manager.js - Gestiona las compras de entradas
 * Permite guardar entradas compradas del usuario en Firestore
 */

class PurchaseManager {
    constructor() {
        this.apiBaseUrl = window.API_BASE_URL || 'http://pil3g3.duckdns.org/api';
    }

    /**
     * Guardar una entrada comprada para el usuario autenticado
     * @param {Object} entrada - Datos de la entrada a guardar
     * Ejemplo: {
     *   evento_id: "evento123",
     *   cantidad_entradas: 2,
     *   precio_total: 50.00,
     *   estado: "confirmada",
     *   fecha_compra: new Date().toISOString()
     * }
     */
    async guardarEntradaComprada(entrada) {
        try {
            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            
            if (!userId) {
                throw new Error('Usuario no autenticado');
            }

            console.log('[PurchaseManager] Guardando entrada para usuario:', userId);
            console.log('[PurchaseManager] Datos de entrada:', entrada);

            const url = `${this.apiBaseUrl}/usuarios/${userId}/entradas-compradas`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(entrada)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error al guardar entrada: ${response.status} ${errorText}`);
            }

            const result = await response.json();
            console.log('[PurchaseManager] Entrada guardada exitosamente:', result);
            
            return result;
        } catch (error) {
            console.error('[PurchaseManager] Error:', error);
            throw error;
        }
    }

    /**
     * Guardar múltiples entradas (para compras de múltiples eventos)
     */
    async guardarMultiplesEntradas(entradas) {
        const resultados = [];
        
        for (const entrada of entradas) {
            try {
                const resultado = await this.guardarEntradaComprada(entrada);
                resultados.push({ success: true, entrada, resultado });
            } catch (error) {
                resultados.push({ success: false, entrada, error: error.message });
            }
        }
        
        return resultados;
    }

    /**
     * Obtener las entradas compradas del usuario
     */
    async obtenerEntradasCompradas() {
        try {
            const userId = localStorage.getItem('userId') || sessionStorage.getItem('userId');
            
            if (!userId) {
                throw new Error('Usuario no autenticado');
            }

            const url = `${this.apiBaseUrl}/usuarios/${userId}/perfil`;
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Error al obtener entradas: ${response.status}`);
            }

            const data = await response.json();
            return data.entradas || [];
        } catch (error) {
            console.error('[PurchaseManager] Error al obtener entradas:', error);
            return [];
        }
    }
}

// Crear instancia global
const purchaseManager = new PurchaseManager();
