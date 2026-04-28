from fastapi import APIRouter, HTTPException, status
from app.services.reserva_espacio_service import ReservaEspacioService
from app.DTOs.reserva_espacio_dto import ReservaEspacioCreate, ReservaEspacioUpdate, ReservaEspacioResponse
from app.utils.exceptions import SubSonicException

router = APIRouter(prefix="/api/espacios", tags=["Reservas de Espacios"])


@router.post("", response_model=ReservaEspacioResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva_espacio(reserva: ReservaEspacioCreate):
    """Crear una nueva reserva de espacio"""
    try:
        return ReservaEspacioService.crear_reserva_espacio(reserva)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{reserva_id}", response_model=ReservaEspacioResponse)
def obtener_reserva_espacio(reserva_id: str):
    """Obtener datos de una reserva de espacio"""
    try:
        return ReservaEspacioService.obtener_reserva_espacio(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[ReservaEspacioResponse])
def obtener_reservas_espacios(skip: int = 0, limit: int = 100):
    """Obtener lista de reservas de espacios"""
    return ReservaEspacioService.obtener_reservas_espacios(skip, limit)


@router.get("/usuario/{usuario_id}", response_model=list[ReservaEspacioResponse])
def obtener_reservas_espacios_usuario(usuario_id: str):
    """Obtener reservas de espacios de un usuario"""
    return ReservaEspacioService.obtener_reservas_espacios_usuario(usuario_id)


@router.get("/tipo/{tipo_espacio}", response_model=list[ReservaEspacioResponse])
def obtener_espacios_por_tipo(tipo_espacio: str):
    """Obtener espacios por tipo"""
    return ReservaEspacioService.obtener_espacios_por_tipo(tipo_espacio)


@router.get("/disponibles/all", response_model=list[ReservaEspacioResponse])
def obtener_espacios_disponibles():
    """Obtener espacios disponibles"""
    return ReservaEspacioService.obtener_espacios_disponibles()


@router.put("/{reserva_id}", response_model=ReservaEspacioResponse)
def actualizar_reserva_espacio(reserva_id: str, reserva_update: ReservaEspacioUpdate):
    """Actualizar una reserva de espacio"""
    try:
        return ReservaEspacioService.actualizar_reserva_espacio(reserva_id, reserva_update)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{reserva_id}/confirmar")
def confirmar_reserva_espacio(reserva_id: str):
    """Confirmar una reserva de espacio"""
    try:
        return ReservaEspacioService.confirmar_reserva_espacio(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva_espacio(reserva_id: str):
    """Cancelar una reserva de espacio"""
    try:
        return ReservaEspacioService.cancelar_reserva_espacio(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{reserva_id}")
def eliminar_reserva_espacio(reserva_id: str):
    """Eliminar una reserva de espacio"""
    try:
        return ReservaEspacioService.eliminar_reserva_espacio(reserva_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
