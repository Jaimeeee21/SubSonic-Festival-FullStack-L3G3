from fastapi import APIRouter, HTTPException, status, Header
from app.services.evento_service import EventoService
from app.DTOs.evento_dto import EventoCreate, EventoUpdate, EventoResponse
from app.utils.exceptions import SubSonicException
from app.utils.auth import get_user_from_token

router = APIRouter(prefix="/api/eventos", tags=["Eventos"])


@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def crear_evento(evento: EventoCreate, authorization: str = Header(None)):
    """Crear un nuevo evento (requiere autenticación)"""
    try:
        user_id = get_user_from_token(authorization)
        return EventoService.crear_evento(evento, user_id=user_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{evento_id}", response_model=EventoResponse)
def obtener_evento(evento_id: str):
    """Obtener datos de un evento"""
    try:
        return EventoService.obtener_evento(evento_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[EventoResponse])
def obtener_eventos(skip: int = 0, limit: int = 100):
    """Obtener lista de eventos"""
    return EventoService.obtener_eventos(skip, limit)


@router.get("/ubicacion/{ubicacion}", response_model=list[EventoResponse])
def obtener_eventos_por_ubicacion(ubicacion: str):
    """Obtener eventos por ubicación"""
    return EventoService.obtener_eventos_por_ubicacion(ubicacion)


@router.put("/{evento_id}", response_model=EventoResponse)
def actualizar_evento(evento_id: str, evento_update: EventoUpdate, authorization: str = Header(None)):
    """Actualizar datos de evento (requiere autenticación)"""
    try:
        user_id = get_user_from_token(authorization)
        return EventoService.actualizar_evento(evento_id, evento_update, user_id=user_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{evento_id}")
def eliminar_evento(evento_id: str, authorization: str = Header(None)):
    """Eliminar un evento (requiere autenticación)"""
    try:
        user_id = get_user_from_token(authorization)
        return EventoService.eliminar_evento(evento_id, user_id=user_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
