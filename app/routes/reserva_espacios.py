"""
app/routes/reserva_espacios.py - Rutas para reserva de espacios de eventos
"""
from fastapi import APIRouter, HTTPException, status, Header, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.firebase import get_firestore
from app.utils.database import get_db
from app.models import Usuario
from datetime import datetime
from typing import Optional, List
import uuid

router = APIRouter(prefix="/api/reservas-espacios", tags=["Reserva de Espacios"])


class CrearReservaRequest(BaseModel):
    """Schema para crear reserva de espacio"""
    evento_id: str
    espacio_id: str
    tipo_espacio: str
    nombre_espacio: str
    tamaño: str
    nombre_negocio: str
    precio: float
    ubicacion_ideales: Optional[List[str]] = None
    servicios_requiere: Optional[List[str]] = None
    descripcion: Optional[str] = None


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_reserva_espacio(
    data: CrearReservaRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva reserva de espacio para un evento
    Guarda DIRECTAMENTE en Firestore
    """
    try:
        # Obtener usuario_id del header
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autorización requerido"
            )

        # Remover "Bearer " si está presente
        usuario_id = authorization.replace("Bearer ", "").strip() if authorization else None

        if not usuario_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        # Buscar usuario en SQL para obtener datos
        usuario = db.query(Usuario).filter(
            (Usuario.id == int(usuario_id) if usuario_id.isdigit() else False) |
            (Usuario.email == usuario_id)
        ).first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )

        # Verificar que es empresa
        if not usuario.es_empresa:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo empresas registradas pueden reservar espacios"
            )

        # GUARDAR DIRECTAMENTE EN FIRESTORE
        firestore_db = get_firestore()
        reserva_id = str(uuid.uuid4())

        reserva_data = {
            'id': reserva_id,
            'usuario_id': usuario.id,
            'usuario_email': usuario.email,
            'empresa_nombre': usuario.empresa_nombre or usuario.nombre,
            'evento_id': data.evento_id,
            'espacio_id': data.espacio_id,
            'tipo_espacio': data.tipo_espacio,
            'nombre_espacio': data.nombre_espacio,
            'tamaño': data.tamaño,
            'descripcion': data.descripcion,
            'nombre_negocio': data.nombre_negocio,
            'precio': data.precio,
            'estado': 'confirmada',
            'ubicacion_ideales': data.ubicacion_ideales or [],
            'servicios_requiere': data.servicios_requiere or [],
            'fecha_reserva': datetime.utcnow().isoformat()
        }

        # Guardar en Firestore
        firestore_db.collection('reservas_espacios').document(reserva_id).set(reserva_data)

        print(f"✅ Reserva guardada en Firestore: {reserva_id}")

        return {
            "success": True,
            "message": f"Espacio '{data.nombre_espacio}' reservado exitosamente",
            "reserva_id": reserva_id,
            "evento_id": data.evento_id,
            "espacio_id": data.espacio_id,
            "estado": "confirmada"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Error en crear_reserva_espacio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear reserva: {str(e)}"
        )


@router.get("/usuario/{usuario_id}")
def obtener_reservas_usuario(usuario_id: str):
    """
    Obtener reservas de un usuario desde Firestore
    Sin order_by para evitar requerimiento de índice compuesto
    """
    try:
        firestore_db = get_firestore()

        # Obtener todas las reservas del usuario desde Firestore (sin order_by)
        docs = firestore_db.collection('reservas_espacios').where(
            'usuario_id', '==', int(usuario_id) if usuario_id.isdigit() else usuario_id
        ).stream()

        reservas = []
        for doc in docs:
            reserva = doc.to_dict()
            reservas.append(reserva)

        # Ordenar en el cliente (en memoria)
        reservas.sort(key=lambda x: x.get('fecha_reserva', ''), reverse=True)

        print(f"✅ Cargadas {len(reservas)} reservas desde Firestore para usuario {usuario_id}")
        return reservas

    except Exception as e:
        print(f"❌ Error en obtener_reservas_usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener reservas: {str(e)}"
        )


@router.get("/usuario/mis-reservas")
def obtener_mis_reservas_deprecated(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    DEPRECADO - Usar GET /usuario/{usuario_id} en su lugar
    """
    raise HTTPException(status_code=status.HTTP_410_GONE, detail="Este endpoint ha sido reemplazado")


@router.get("/{reserva_id}")
def obtener_reserva(reserva_id: str):
    """
    Obtener detalles de una reserva específica desde Firestore
    """
    try:
        firestore_db = get_firestore()
        doc = firestore_db.collection('reservas_espacios').document(reserva_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        
        return doc.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: str, authorization: str = Header(None)):
    """
    Cancelar una reserva de espacio
    """
    try:
        firestore_db = get_firestore()
        
        # Obtener reserva
        doc = firestore_db.collection('reservas_espacios').document(reserva_id).get()
        if not doc.exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Actualizar estado
        firestore_db.collection('reservas_espacios').document(reserva_id).update({
            'estado': 'cancelada'
        })
        
        return {
            "success": True,
            "message": "Reserva cancelada exitosamente",
            "reserva_id": reserva_id,
            "estado": "cancelada"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/todas/lista")
def obtener_todas_reservas():
    """
    Obtener TODAS las reservas de espacios del sistema (para admin)
    Retorna lista de todas las reservas ordenadas por fecha
    """
    try:
        firestore_db = get_firestore()
        
        # Obtener todas las reservas de la colección
        reservas_docs = firestore_db.collection('reservas_espacios').stream()
        reservas = []
        
        for doc in reservas_docs:
            reserva_data = doc.to_dict()
            reserva_data['id'] = doc.id
            reservas.append(reserva_data)
        
        # Ordenar por fecha (más recientes primero)
        reservas.sort(key=lambda x: x.get('fecha_reserva', ''), reverse=True)
        
        return reservas
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener reservas: {str(e)}"
        )
