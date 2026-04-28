from app.dao.usuario_dao import UsuarioDAO
from app.dao.reserva_dao import ReservaDAO
from app.DTOs.usuario_dto import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioPerfil
from app.utils.exceptions import UnauthorizedException


class UsuarioService:
    """Service para la lógica de negocio de Usuarios (usando Firestore)"""

    @staticmethod
    def registrar_usuario(usuario: UsuarioCreate) -> UsuarioResponse:
        """Registrar un nuevo usuario"""
        # Aquí se podría agregar lógica de negocio como encriptación de contraseña
        db_usuario = UsuarioDAO.create(usuario)
        return UsuarioResponse(**db_usuario)

    @staticmethod
    def login(email: str, password: str) -> UsuarioResponse:
        """Validar credenciales de login"""
        usuario = UsuarioDAO.get_by_email(email)
        
        # Aquí se debería validar la contraseña con hash
        # Por ahora es simple comparación (MEJORAR EN PRODUCCIÓN)
        if usuario.get('password') != password:
            raise UnauthorizedException("Credenciales inválidas")
        
        return UsuarioResponse(**usuario)

    @staticmethod
    def obtener_usuario(usuario_id: str) -> UsuarioResponse:
        """Obtener datos de un usuario"""
        usuario = UsuarioDAO.get_by_id(usuario_id)
        return UsuarioResponse(**usuario)

    @staticmethod
    def obtener_usuarios(skip: int = 0, limit: int = 100) -> list[UsuarioResponse]:
        """Obtener lista de usuarios"""
        usuarios = UsuarioDAO.get_all(skip, limit)
        return [UsuarioResponse(**u) for u in usuarios]

    @staticmethod
    def actualizar_usuario(usuario_id: str, usuario_update: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar datos de usuario"""
        usuario = UsuarioDAO.update(usuario_id, usuario_update)
        return UsuarioResponse(**usuario)

    @staticmethod
    def eliminar_usuario(usuario_id: str) -> dict:
        """Eliminar un usuario"""
        UsuarioDAO.delete(usuario_id)
        return {"mensaje": "Usuario eliminado correctamente"}

    @staticmethod
    def obtener_por_email(email: str) -> UsuarioResponse:
        """Obtener usuario por email"""
        usuario = UsuarioDAO.get_by_email(email)
        return UsuarioResponse(**usuario)

    @staticmethod
    def obtener_perfil(usuario_id: str) -> dict:
        """Obtener el perfil completo del usuario con datos de entradas"""
        usuario = UsuarioDAO.get_perfil(usuario_id)
        
        # Obtener reservas (entradas compradas) del usuario
        reservas = ReservaDAO.get_by_usuario(usuario_id)
        
        return {
            "usuario": usuario,
            "entradas": reservas
        }

    @staticmethod
    def actualizar_foto_perfil(usuario_id: str, foto_url: str) -> dict:
        """Actualizar la foto de perfil de un usuario"""
        usuario = UsuarioDAO.update_foto_perfil(usuario_id, foto_url)
        return usuario

    @staticmethod
    def agregar_entrada_comprada(usuario_id: str, entrada: dict) -> dict:
        """Agregar una entrada comprada al usuario"""
        return UsuarioDAO.agregar_entrada_comprada(usuario_id, entrada)

