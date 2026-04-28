from fastapi import APIRouter, HTTPException, status
from app.services.reserva_service import ReservaService
from app.DTOs.reserva_dto import ReservaCreate, ReservaUpdate, ReservaResponse
from app.utils.exceptions import SubSonicException

router = APIRouter(prefix="/api/reservas", tags=["Reservas de Tickets"])


@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: ReservaCreate):
    """Crear una nueva reserva de tickets"""
    try:
        return ReservaService.crear_reserva(reserva)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: str):
    """Obtener datos de una reserva"""
    try:
        return ReservaService.obtener_reserva(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[ReservaResponse])
def obtener_reservas(skip: int = 0, limit: int = 100):
    """Obtener lista de reservas"""
    return ReservaService.obtener_reservas(skip, limit)


@router.get("/usuario/{usuario_id}", response_model=list[ReservaResponse])
def obtener_reservas_usuario(usuario_id: str):
    """Obtener reservas de un usuario"""
    return ReservaService.obtener_reservas_usuario(usuario_id)


@router.get("/evento/{evento_id}", response_model=list[ReservaResponse])
def obtener_reservas_evento(evento_id: str):
    """Obtener reservas de un evento"""
    return ReservaService.obtener_reservas_evento(evento_id)


@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar_reserva(reserva_id: str, reserva_update: ReservaUpdate):
    """Actualizar una reserva"""
    try:
        return ReservaService.actualizar_reserva(reserva_id, reserva_update)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{reserva_id}/confirmar")
def confirmar_reserva(reserva_id: str):
    """Confirmar una reserva"""
    try:
        return ReservaService.confirmar_reserva(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: str):
    """Cancelar una reserva"""
    try:
        return ReservaService.cancelar_reserva(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: str):
    """Eliminar una reserva"""
    try:
        return ReservaService.eliminar_reserva(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
