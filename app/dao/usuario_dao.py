from app.utils.firebase import get_firestore
from app.DTOs.usuario_dto import UsuarioCreate, UsuarioUpdate
from app.utils.exceptions import NotFoundException, ConflictException, DatabaseException


class UsuarioDAO:
    """Data Access Object para Usuario (usando Firestore)"""

    COLLECTION = "usuarios"

    @staticmethod
    def create(usuario: UsuarioCreate) -> dict:
        """Crear un nuevo usuario en Firestore"""
        try:
            db = get_firestore()
            usuario_dict = usuario.dict()
            
            # Verificar si el email ya existe
            docs = db.collection(UsuarioDAO.COLLECTION).where("email", "==", usuario_dict["email"]).stream()
            if any(docs):
                raise ConflictException(f"Email {usuario_dict['email']} ya existe")
            
            # Generar ID si no existe
            if not usuario_dict.get("id"):
                usuario_dict["id"] = db.collection(UsuarioDAO.COLLECTION).document().id
            
            doc_ref = db.collection(UsuarioDAO.COLLECTION).document(usuario_dict["id"])
            doc_ref.set(usuario_dict)
            
            return usuario_dict
        except ConflictException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al crear usuario: {str(e)}")

    @staticmethod
    def get_by_id(usuario_id: str) -> dict:
        """Obtener usuario por ID desde Firestore"""
        try:
            db = get_firestore()
            doc = db.collection(UsuarioDAO.COLLECTION).document(usuario_id).get()
            
            if not doc.exists:
                raise NotFoundException(f"Usuario con ID {usuario_id} no encontrado")
            
            return doc.to_dict()
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener usuario: {str(e)}")

    @staticmethod
    def get_by_email(email: str) -> dict:
        """Obtener usuario por email desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(UsuarioDAO.COLLECTION).where("email", "==", email).stream()
            
            for doc in docs:
                return doc.to_dict()
            
            raise NotFoundException(f"Usuario con email {email} no encontrado")
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener usuario: {str(e)}")

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> list:
        """Obtener todos los usuarios desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(UsuarioDAO.COLLECTION).offset(skip).limit(limit).stream()
            
            usuarios = []
            for doc in docs:
                usuarios.append(doc.to_dict())
            
            return usuarios
        except Exception as e:
            raise DatabaseException(f"Error al obtener usuarios: {str(e)}")

    @staticmethod
    def update(usuario_id: str, usuario_update: UsuarioUpdate) -> dict:
        """Actualizar usuario en Firestore"""
        try:
            db = get_firestore()
            usuario = UsuarioDAO.get_by_id(usuario_id)
            
            update_data = usuario_update.dict(exclude_unset=True)
            usuario.update(update_data)
            
            db.collection(UsuarioDAO.COLLECTION).document(usuario_id).update(update_data)
            
            return usuario
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar usuario: {str(e)}")

    @staticmethod
    def delete(usuario_id: str) -> bool:
        """Eliminar usuario de Firestore"""
        try:
            db = get_firestore()
            UsuarioDAO.get_by_id(usuario_id)  # Verificar que existe
            
            db.collection(UsuarioDAO.COLLECTION).document(usuario_id).delete()
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar usuario: {str(e)}")

    @staticmethod
    def update_foto_perfil(usuario_id: str, foto_url: str) -> dict:
        """Actualizar la foto de perfil de un usuario"""
        try:
            db = get_firestore()
            usuario = UsuarioDAO.get_by_id(usuario_id)  # Verificar que existe
            
            db.collection(UsuarioDAO.COLLECTION).document(usuario_id).update({
                "foto_perfil": foto_url
            })
            
            usuario["foto_perfil"] = foto_url
            return usuario
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar foto de perfil: {str(e)}")

    @staticmethod
    def get_perfil(usuario_id: str) -> dict:
        """Obtener el perfil completo de un usuario"""
        try:
            usuario = UsuarioDAO.get_by_id(usuario_id)
            # Excluir campos sensibles como password
            usuario_perfil = {k: v for k, v in usuario.items() if k != 'password'}
            return usuario_perfil
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener perfil: {str(e)}")

    @staticmethod
    def agregar_entrada_comprada(usuario_id: str, entrada: dict) -> dict:
        """Agregar una entrada comprada al usuario"""
        try:
            db = get_firestore()
            usuario = UsuarioDAO.get_by_id(usuario_id)
            
            # Inicializar lista de entradas si no existe
            if 'entradas_compradas' not in usuario:
                usuario['entradas_compradas'] = []
            
            # Agregar la entrada a la lista
            usuario['entradas_compradas'].append(entrada)
            
            # Actualizar en Firestore
            db.collection(UsuarioDAO.COLLECTION).document(usuario_id).update({
                'entradas_compradas': usuario['entradas_compradas']
            })
            
            return usuario
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al agregar entrada comprada: {str(e)}")
