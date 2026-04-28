from app.dao.evento_dao import EventoDAO
from app.DTOs.evento_dto import EventoCreate, EventoUpdate, EventoResponse


class EventoService:
    """Service para la lógica de negocio de Eventos (usando Firestore)"""

    @staticmethod
    def crear_evento(evento: EventoCreate) -> EventoResponse:
        """Crear un nuevo evento"""
        db_evento = EventoDAO.create(evento)
        return EventoResponse(**db_evento)

    @staticmethod
    def obtener_evento(evento_id: str) -> EventoResponse:
        """Obtener datos de un evento"""
        evento = EventoDAO.get_by_id(evento_id)
        return EventoResponse(**evento)

    @staticmethod
    def obtener_eventos(skip: int = 0, limit: int = 100) -> list[EventoResponse]:
        """Obtener lista de eventos"""
        eventos = EventoDAO.get_all(skip, limit)
        return [EventoResponse(**e) for e in eventos]

    @staticmethod
    def obtener_eventos_por_ubicacion(ubicacion: str) -> list[EventoResponse]:
        """Obtener eventos por ubicación"""
        eventos = EventoDAO.get_by_ubicacion(ubicacion)
        return [EventoResponse(**e) for e in eventos]

    @staticmethod
    def actualizar_evento(evento_id: str, evento_update: EventoUpdate) -> EventoResponse:
        """Actualizar datos de evento"""
        evento = EventoDAO.update(evento_id, evento_update)
        return EventoResponse(**evento)

    @staticmethod
    def eliminar_evento(evento_id: str) -> dict:
        """Eliminar un evento"""
        EventoDAO.delete(evento_id)
        return {"mensaje": "Evento eliminado correctamente"}
