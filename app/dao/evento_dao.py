from app.utils.firebase import get_firestore
from app.DTOs.evento_dto import EventoCreate, EventoUpdate
from app.utils.exceptions import NotFoundException, DatabaseException


class EventoDAO:
    """Data Access Object para Evento (usando Firestore)"""

    COLLECTION = "eventos"

    @staticmethod
    def create(evento: EventoCreate) -> dict:
        """Crear un nuevo evento en Firestore"""
        try:
            db = get_firestore()
            evento_dict = evento.dict()
            
            # Si no tiene ID, generar uno
            if not evento_dict.get("id"):
                evento_dict["id"] = db.collection(EventoDAO.COLLECTION).document().id
            
            doc_ref = db.collection(EventoDAO.COLLECTION).document(evento_dict["id"])
            doc_ref.set(evento_dict)
            
            return evento_dict
        except Exception as e:
            raise DatabaseException(f"Error al crear evento: {str(e)}")

    @staticmethod
    def get_by_id(evento_id: str) -> dict:
        """Obtener evento por ID desde Firestore"""
        try:
            db = get_firestore()
            doc = db.collection(EventoDAO.COLLECTION).document(evento_id).get()
            
            if not doc.exists:
                raise NotFoundException(f"Evento con ID {evento_id} no encontrado")
            
            return doc.to_dict()
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener evento: {str(e)}")

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> list:
        """Obtener todos los eventos desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(EventoDAO.COLLECTION).offset(skip).limit(limit).stream()
            
            eventos = []
            for doc in docs:
                eventos.append(doc.to_dict())
            
            return eventos
        except Exception as e:
            raise DatabaseException(f"Error al obtener eventos: {str(e)}")

    @staticmethod
    def get_by_ubicacion(ubicacion: str) -> list:
        """Obtener eventos por ubicación desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(EventoDAO.COLLECTION).where("ubicacion", "==", ubicacion).stream()
            
            eventos = []
            for doc in docs:
                eventos.append(doc.to_dict())
            
            return eventos
        except Exception as e:
            raise DatabaseException(f"Error al obtener eventos por ubicación: {str(e)}")

    @staticmethod
    def update(evento_id: str, evento_update: EventoUpdate) -> dict:
        """Actualizar evento en Firestore"""
        try:
            db = get_firestore()
            evento = EventoDAO.get_by_id(evento_id)
            
            update_data = evento_update.dict(exclude_unset=True)
            evento.update(update_data)
            
            db.collection(EventoDAO.COLLECTION).document(evento_id).update(update_data)
            
            return evento
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar evento: {str(e)}")

    @staticmethod
    def delete(evento_id: str) -> bool:
        """Eliminar evento de Firestore"""
        try:
            db = get_firestore()
            EventoDAO.get_by_id(evento_id)  # Verificar que existe
            
            db.collection(EventoDAO.COLLECTION).document(evento_id).delete()
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar evento: {str(e)}")
