from app.utils.firebase import get_firestore
from app.DTOs.reserva_dto import ReservaCreate, ReservaUpdate
from app.utils.exceptions import NotFoundException, DatabaseException


class ReservaDAO:
    """Data Access Object para Reserva de tickets (usando Firestore)"""

    COLLECTION = "reservas"

    @staticmethod
    def create(reserva: ReservaCreate) -> dict:
        """Crear una nueva reserva en Firestore"""
        try:
            db = get_firestore()
            reserva_dict = reserva.dict()
            
            # Generar ID si no existe
            if not reserva_dict.get("id"):
                reserva_dict["id"] = db.collection(ReservaDAO.COLLECTION).document().id
            
            doc_ref = db.collection(ReservaDAO.COLLECTION).document(reserva_dict["id"])
            doc_ref.set(reserva_dict)
            
            return reserva_dict
        except Exception as e:
            raise DatabaseException(f"Error al crear reserva: {str(e)}")

    @staticmethod
    def get_by_id(reserva_id: str) -> dict:
        """Obtener reserva por ID desde Firestore"""
        try:
            db = get_firestore()
            doc = db.collection(ReservaDAO.COLLECTION).document(reserva_id).get()
            
            if not doc.exists:
                raise NotFoundException(f"Reserva con ID {reserva_id} no encontrada")
            
            return doc.to_dict()
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener reserva: {str(e)}")

    @staticmethod
    def get_by_usuario(usuario_id: str) -> list:
        """Obtener todas las reservas de un usuario desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaDAO.COLLECTION).where("usuario_id", "==", usuario_id).stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener reservas del usuario: {str(e)}")

    @staticmethod
    def get_by_evento(evento_id: str) -> list:
        """Obtener todas las reservas de un evento desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaDAO.COLLECTION).where("evento_id", "==", evento_id).stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener reservas del evento: {str(e)}")

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> list:
        """Obtener todas las reservas desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaDAO.COLLECTION).offset(skip).limit(limit).stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener reservas: {str(e)}")

    @staticmethod
    def update(reserva_id: str, reserva_update: ReservaUpdate) -> dict:
        """Actualizar reserva en Firestore"""
        try:
            db = get_firestore()
            reserva = ReservaDAO.get_by_id(reserva_id)
            
            update_data = reserva_update.dict(exclude_unset=True)
            reserva.update(update_data)
            
            db.collection(ReservaDAO.COLLECTION).document(reserva_id).update(update_data)
            
            return reserva
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar reserva: {str(e)}")

    @staticmethod
    def delete(reserva_id: str) -> bool:
        """Eliminar reserva de Firestore"""
        try:
            db = get_firestore()
            ReservaDAO.get_by_id(reserva_id)  # Verificar que existe
            
            db.collection(ReservaDAO.COLLECTION).document(reserva_id).delete()
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar reserva: {str(e)}")
