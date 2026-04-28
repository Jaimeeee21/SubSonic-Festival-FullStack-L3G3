/**
 * EJEMPLO DE USO: Guardar entradas compradas
 * 
 * Este archivo muestra cómo usar el sistema para guardar entradas
 * que un usuario compra en la plataforma.
 */

// EJEMPLO 1: Guardar una entrada después de comprar en eventos.html
async function comprarEntrada(eventoId, cantidadEntradas, precioTotal) {
    try {
        // Datos de la entrada a guardar
        const entrada = {
            evento_id: eventoId,
            cantidad_entradas: cantidadEntradas,
            precio_total: precioTotal,
            estado: "confirmada",
            fecha_compra: new Date().toISOString(),
            numero_transaccion: "TRX_" + Date.now()
        };

        console.log('[COMPRA] Guardando entrada:', entrada);

        // Guardar la entrada usando purchaseManager
        const resultado = await purchaseManager.guardarEntradaComprada(entrada);
        
        console.log('[COMPRA] Entrada guardada exitosamente:', resultado);
        alert('¡Entrada comprada y guardada!');
        
    } catch (error) {
        console.error('[COMPRA] Error:', error);
        alert('Error al guardar la entrada: ' + error.message);
    }
}

// EJEMPLO 2: Guardar múltiples entradas (carrito con varios eventos)
async function comprarMultiplesEventos(carrito) {
    try {
        // carrito = [{evento_id: '1', cantidad: 2, precio: 50}, {...}]
        
        const entradas = carrito.map(item => ({
            evento_id: item.evento_id,
            cantidad_entradas: item.cantidad,
            precio_total: item.precio,
            estado: "confirmada",
            fecha_compra: new Date().toISOString(),
            numero_transaccion: "TRX_" + Date.now()
        }));

        console.log('[CARRITO] Procesando', entradas.length, 'entradas');

        const resultados = await purchaseManager.guardarMultiplesEntradas(entradas);
        
        // Verificar resultados
        const exitosas = resultados.filter(r => r.success).length;
        const fallidas = resultados.filter(r => !r.success).length;
        
        console.log(`[CARRITO] ${exitosas} exitosas, ${fallidas} fallidas`);
        alert(`Se guardaron ${exitosas} entradas correctamente`);
        
    } catch (error) {
        console.error('[CARRITO] Error:', error);
    }
}

// EJEMPLO 3: Obtener las entradas que el usuario ha comprado
async function mostrarMisEntradas() {
    try {
        const entradas = await purchaseManager.obtenerEntradasCompradas();
        
        console.log('[MIS ENTRADAS]', entradas);
        
        if (entradas.length === 0) {
            console.log('No tienes entradas compradas aún');
        } else {
            console.log(`Tienes ${entradas.length} entrada(s) comprada(s):`);
            entradas.forEach((entrada, index) => {
                console.log(`${index + 1}. ${entrada.evento_id} - ${entrada.cantidad_entradas} entrada(s) - $${entrada.precio_total}`);
            });
        }
        
        return entradas;
        
    } catch (error) {
        console.error('[MIS ENTRADAS] Error:', error);
    }
}

/**
 * EJEMPLO DE ESTRUCTURA EN FIRESTORE:
 * 
 * Colección: usuarios
 * Documento: suarezpitel@gmail.com
 * {
 *   email: "suarezpitel@gmail.com"
 *   nombre: "josemanuelsp2005"
 *   tipo_auth: "email"
 *   created_at: 2026-04-24T12:51:01.710911
 *   entradas_compradas: [
 *     {
 *       evento_id: "evento_madrid_001",
 *       cantidad_entradas: 2,
 *       precio_total: 50.00,
 *       estado: "confirmada",
 *       fecha_compra: "2026-04-24T15:30:00.000Z",
 *       numero_transaccion: "TRX_1714008600000"
 *     },
 *     {
 *       evento_id: "evento_barcelona_002",
 *       cantidad_entradas: 1,
 *       precio_total: 25.00,
 *       estado: "confirmada",
 *       fecha_compra: "2026-04-24T16:15:00.000Z",
 *       numero_transaccion: "TRX_1714012100000"
 *     }
 *   ]
 * }
 */

// Para usar en eventos.html, por ejemplo:
// 1. Agregar purchase-manager.js al HTML
// 2. Cuando el usuario confirma una compra, llamar:
//    comprarEntrada("evento_id", 2, 50.00);
// 3. Las entradas se guardarán en entradas_compradas[]
