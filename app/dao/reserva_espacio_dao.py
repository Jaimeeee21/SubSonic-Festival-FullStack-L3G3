from app.utils.firebase import get_firestore
from app.DTOs.reserva_espacio_dto import ReservaEspacioCreate, ReservaEspacioUpdate
from app.utils.exceptions import NotFoundException, DatabaseException


class ReservaEspacioDAO:
    """Data Access Object para Reserva de Espacios (usando Firestore)"""

    COLLECTION = "reservas_espacios"

    @staticmethod
    def create(reserva_espacio: ReservaEspacioCreate) -> dict:
        """Crear una nueva reserva de espacio en Firestore"""
        try:
            db = get_firestore()
            reserva_dict = reserva_espacio.dict()
            
            # Generar ID si no existe
            if not reserva_dict.get("id"):
                reserva_dict["id"] = db.collection(ReservaEspacioDAO.COLLECTION).document().id
            
            doc_ref = db.collection(ReservaEspacioDAO.COLLECTION).document(reserva_dict["id"])
            doc_ref.set(reserva_dict)
            
            return reserva_dict
        except Exception as e:
            raise DatabaseException(f"Error al crear reserva de espacio: {str(e)}")

    @staticmethod
    def get_by_id(reserva_id: str) -> dict:
        """Obtener reserva por ID desde Firestore"""
        try:
            db = get_firestore()
            doc = db.collection(ReservaEspacioDAO.COLLECTION).document(reserva_id).get()
            
            if not doc.exists:
                raise NotFoundException(f"Reserva de espacio con ID {reserva_id} no encontrada")
            
            return doc.to_dict()
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener reserva de espacio: {str(e)}")

    @staticmethod
    def get_by_usuario(usuario_id: str) -> list:
        """Obtener todas las reservas de espacios de un usuario desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaEspacioDAO.COLLECTION).where("usuario_id", "==", usuario_id).stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener reservas de espacios del usuario: {str(e)}")

    @staticmethod
    def get_by_tipo(tipo_espacio: str) -> list:
        """Obtener reservas por tipo de espacio desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaEspacioDAO.COLLECTION).where("tipo_espacio", "==", tipo_espacio).stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener reservas por tipo: {str(e)}")

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> list:
        """Obtener todas las reservas de espacios desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaEspacioDAO.COLLECTION).offset(skip).limit(limit).stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener reservas de espacios: {str(e)}")

    @staticmethod
    def get_disponibles() -> list:
        """Obtener espacios disponibles desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ReservaEspacioDAO.COLLECTION).where("estado", "==", "disponible").stream()
            
            reservas = []
            for doc in docs:
                reservas.append(doc.to_dict())
            
            return reservas
        except Exception as e:
            raise DatabaseException(f"Error al obtener espacios disponibles: {str(e)}")

    @staticmethod
    def update(reserva_id: str, reserva_update: ReservaEspacioUpdate) -> dict:
        """Actualizar reserva de espacio en Firestore"""
        try:
            db = get_firestore()
            reserva = ReservaEspacioDAO.get_by_id(reserva_id)
            
            update_data = reserva_update.dict(exclude_unset=True)
            reserva.update(update_data)
            
            db.collection(ReservaEspacioDAO.COLLECTION).document(reserva_id).update(update_data)
            
            return reserva
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar reserva de espacio: {str(e)}")

    @staticmethod
    def delete(reserva_id: str) -> bool:
        """Eliminar reserva de espacio de Firestore"""
        try:
            db = get_firestore()
            ReservaEspacioDAO.get_by_id(reserva_id)  # Verificar que existe
            
            db.collection(ReservaEspacioDAO.COLLECTION).document(reserva_id).delete()
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar reserva de espacio: {str(e)}")
