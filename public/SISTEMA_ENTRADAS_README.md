# 📋 Sistema de Entradas Compradas - SUBSONIC Festival

## ✅ Estado Actual

El sistema de entradas compradas está **completamente implementado** y funcional.

### Campos en Firestore

Cada usuario en la colección `usuarios` ahora tiene:

```
email: "suarezpitel@gmail.com"
nombre: "josemanuelsp2005"
tipo_auth: "email" o "google"
created_at: DateTime (fecha de creación de la cuenta)
entradas_compradas: Array [...]  ← AQUÍ SE GUARDAN LAS COMPRAS
```

### ¿Dónde se guardan las entradas?

Las entradas compradas se guardan en el campo **`entradas_compradas`** de cada usuario, como un array:

```javascript
entradas_compradas: [
  {
    evento_id: "evento123",
    cantidad_entradas: 2,
    precio_total: 50.00,
    estado: "confirmada",
    fecha_compra: "2026-04-24T15:30:00.000Z"
  }
]
```

## 🚀 Cómo Usar (Para Desarrolladores)

### 1. Guardar UNA entrada cuando se compra

```javascript
// En cualquier página donde esté cargado purchase-manager.js
await purchaseManager.guardarEntradaComprada({
    evento_id: "evento_madrid_001",
    cantidad_entradas: 2,
    precio_total: 50.00,
    estado: "confirmada",
    fecha_compra: new Date().toISOString()
});
```

### 2. Guardar MÚLTIPLES entradas (carrito)

```javascript
const resultados = await purchaseManager.guardarMultiplesEntradas([
    { evento_id: "evento1", cantidad_entradas: 1, precio_total: 25 },
    { evento_id: "evento2", cantidad_entradas: 2, precio_total: 50 }
]);
```

### 3. Obtener las entradas del usuario

```javascript
const miasEntradas = await purchaseManager.obtenerEntradasCompradas();
console.log(miasEntradas);
```

## 📍 Dónde está implementado

### Backend (Python FastAPI)
- **Endpoint**: `POST /api/usuarios/{usuario_id}/entradas-compradas`
- **Archivo**: `app/routes/usuarios.py`
- **DAO**: `app/dao/usuario_dao.py` (método `agregar_entrada_comprada`)

### Frontend (JavaScript)
- **Archivo**: `public/purchase-manager.js`
- **Cargado en**: eventos.html, evento-detail.html, cart.html, profile.html

## 🔄 Flujo Completo de Compra

1. Usuario se autentica y obtiene su `userId` (email)
2. Usuario compra entradas en eventos.html o evento-detail.html
3. Sistema llama `purchaseManager.guardarEntradaComprada(datos)`
4. Datos se envían a `POST /api/usuarios/{userId}/entradas-compradas`
5. Backend agrega la entrada al array `entradas_compradas` en Firestore
6. Cuando usuario ve su perfil, se cargan y muestran sus entradas

## 📊 Ejemplo en Firestore (Console)

```
usuarios/
├── suarezpitel@gmail.com
│   ├── email: "suarezpitel@gmail.com"
│   ├── nombre: "josemanuelsp2005"
│   ├── created_at: 2026-04-24...
│   ├── entradas_compradas: [
│   │   {
│   │     evento_id: "madrid_concierto_001"
│   │     cantidad_entradas: 2
│   │     precio_total: 60
│   │     estado: "confirmada"
│   │     fecha_compra: "2026-04-24T15:30..."
│   │   },
│   │   {
│   │     evento_id: "barcelona_festival_002"
│   │     cantidad_entradas: 1
│   │     precio_total: 40
│   │     estado: "confirmada"
│   │     fecha_compra: "2026-04-24T16:15..."
│   │   }
│   └── ]
│   └── tipo_auth: "email"
```

## 🎯 Próximos Pasos (Opcionales)

1. Integrar con pasarela de pago real (Stripe, PayPal, etc.)
2. Enviar email de confirmación con detalles de la entrada
3. Generar código QR para cada entrada
4. Permitir cancelación/reembolso de entradas
5. Dashboard de entradas en perfil más detallado

## 💡 Notas Importantes

- El campo `creado_en` fue eliminado (quedó solo `created_at`)
- Cada usuario autenticado tiene `entradas_compradas: []` inicializado
- Las entradas se almacenan como un array dentro del documento del usuario (denormalización)
- El sistema usa el email como identificador único del usuario

---

**Estado**: ✅ Producción | **Versión**: 1.0 | **Última actualización**: 24-04-2026
