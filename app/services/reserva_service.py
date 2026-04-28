from app.dao.reserva_dao import ReservaDAO
from app.DTOs.reserva_dto import ReservaCreate, ReservaUpdate, ReservaResponse


class ReservaService:
    """Service para la lógica de negocio de Reservas de Tickets (usando Firestore)"""

    @staticmethod
    def crear_reserva(reserva: ReservaCreate) -> ReservaResponse:
        """Crear una nueva reserva de tickets"""
        # Aquí se podría agregar lógica de validación de disponibilidad
        db_reserva = ReservaDAO.create(reserva)
        return ReservaResponse(**db_reserva)

    @staticmethod
    def obtener_reserva(reserva_id: str) -> ReservaResponse:
        """Obtener datos de una reserva"""
        reserva = ReservaDAO.get_by_id(reserva_id)
        return ReservaResponse(**reserva)

    @staticmethod
    def obtener_reservas_usuario(usuario_id: str) -> list[ReservaResponse]:
        """Obtener todas las reservas de un usuario"""
        reservas = ReservaDAO.get_by_usuario(usuario_id)
        return [ReservaResponse(**r) for r in reservas]

    @staticmethod
    def obtener_reservas_evento(evento_id: str) -> list[ReservaResponse]:
        """Obtener todas las reservas de un evento"""
        reservas = ReservaDAO.get_by_evento(evento_id)
        return [ReservaResponse(**r) for r in reservas]

    @staticmethod
    def obtener_reservas(skip: int = 0, limit: int = 100) -> list[ReservaResponse]:
        """Obtener lista de reservas"""
        reservas = ReservaDAO.get_all(skip, limit)
        return [ReservaResponse(**r) for r in reservas]

    @staticmethod
    def actualizar_reserva(reserva_id: str, reserva_update: ReservaUpdate) -> ReservaResponse:
        """Actualizar una reserva (ej: cambiar estado a confirmada/cancelada)"""
        reserva = ReservaDAO.update(reserva_id, reserva_update)
        return ReservaResponse(**reserva)

    @staticmethod
    def cancelar_reserva(reserva_id: str) -> dict:
        """Cancelar una reserva"""
        reserva_update = ReservaUpdate(estado="cancelada")
        ReservaDAO.update(reserva_id, reserva_update)
        return {"mensaje": "Reserva cancelada correctamente"}

    @staticmethod
    def confirmar_reserva(reserva_id: str) -> dict:
        """Confirmar una reserva"""
        reserva_update = ReservaUpdate(estado="confirmada")
        ReservaDAO.update(reserva_id, reserva_update)
        return {"mensaje": "Reserva confirmada correctamente"}

    @staticmethod
    def eliminar_reserva(reserva_id: str) -> dict:
        """Eliminar una reserva"""
        ReservaDAO.delete(reserva_id)
        return {"mensaje": "Reserva eliminada correctamente"}
