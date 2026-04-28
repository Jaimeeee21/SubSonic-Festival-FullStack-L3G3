from app.dao.reserva_espacio_dao import ReservaEspacioDAO
from app.DTOs.reserva_espacio_dto import ReservaEspacioCreate, ReservaEspacioUpdate, ReservaEspacioResponse


class ReservaEspacioService:
    """Service para la lógica de negocio de Reservas de Espacios (usando Firestore)"""

    @staticmethod
    def crear_reserva_espacio(reserva: ReservaEspacioCreate) -> ReservaEspacioResponse:
        """Crear una nueva reserva de espacio"""
        db_reserva = ReservaEspacioDAO.create(reserva)
        return ReservaEspacioResponse(**db_reserva)

    @staticmethod
    def obtener_reserva_espacio(reserva_id: str) -> ReservaEspacioResponse:
        """Obtener datos de una reserva de espacio"""
        reserva = ReservaEspacioDAO.get_by_id(reserva_id)
        return ReservaEspacioResponse(**reserva)

    @staticmethod
    def obtener_reservas_espacios_usuario(usuario_id: str) -> list[ReservaEspacioResponse]:
        """Obtener todas las reservas de espacios de un usuario"""
        reservas = ReservaEspacioDAO.get_by_usuario(usuario_id)
        return [ReservaEspacioResponse(**r) for r in reservas]

    @staticmethod
    def obtener_espacios_por_tipo(tipo_espacio: str) -> list[ReservaEspacioResponse]:
        """Obtener espacios por tipo"""
        espacios = ReservaEspacioDAO.get_by_tipo(tipo_espacio)
        return [ReservaEspacioResponse(**e) for e in espacios]

    @staticmethod
    def obtener_espacios_disponibles() -> list[ReservaEspacioResponse]:
        """Obtener espacios disponibles"""
        espacios = ReservaEspacioDAO.get_disponibles()
        return [ReservaEspacioResponse(**e) for e in espacios]

    @staticmethod
    def obtener_reservas_espacios(skip: int = 0, limit: int = 100) -> list[ReservaEspacioResponse]:
        """Obtener lista de reservas de espacios"""
        reservas = ReservaEspacioDAO.get_all(skip, limit)
        return [ReservaEspacioResponse(**r) for r in reservas]

    @staticmethod
    def actualizar_reserva_espacio(reserva_id: str, reserva_update: ReservaEspacioUpdate) -> ReservaEspacioResponse:
        """Actualizar una reserva de espacio"""
        reserva = ReservaEspacioDAO.update(reserva_id, reserva_update)
        return ReservaEspacioResponse(**reserva)

    @staticmethod
    def confirmar_reserva_espacio(reserva_id: str) -> dict:
        """Confirmar una reserva de espacio"""
        reserva_update = ReservaEspacioUpdate(estado="confirmada")
        ReservaEspacioDAO.update(reserva_id, reserva_update)
        return {"mensaje": "Reserva de espacio confirmada correctamente"}

    @staticmethod
    def cancelar_reserva_espacio(reserva_id: str) -> dict:
        """Cancelar una reserva de espacio"""
        reserva_update = ReservaEspacioUpdate(estado="cancelada")
        ReservaEspacioDAO.update(reserva_id, reserva_update)
        return {"mensaje": "Reserva de espacio cancelada correctamente"}

    @staticmethod
    def eliminar_reserva_espacio(reserva_id: str) -> dict:
        """Eliminar una reserva de espacio"""
        ReservaEspacioDAO.delete(reserva_id)
        return {"mensaje": "Reserva de espacio eliminada correctamente"}
