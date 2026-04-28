from app.dao.usuario_dao import UsuarioDAO
from app.dao.evento_dao import EventoDAO
from app.dao.producto_dao import ProductoDAO
from app.dao.reserva_dao import ReservaDAO
from app.dao.reserva_espacio_dao import ReservaEspacioDAO


class DAOFactory:
    """Factory para crear instancias de DAOs"""

    _daos = {
        'usuario': UsuarioDAO,
        'evento': EventoDAO,
        'producto': ProductoDAO,
        'reserva': ReservaDAO,
        'reserva_espacio': ReservaEspacioDAO,
    }

    @classmethod
    def create_dao(cls, dao_type: str):
        """
        Crear una instancia de DAO por tipo
        
        Args:
            dao_type: Tipo de DAO a crear (usuario, evento, producto, reserva, reserva_espacio)
        
        Returns:
            Instancia del DAO solicitado
        """
        dao_class = cls._daos.get(dao_type.lower())
        if not dao_class:
            raise ValueError(f"DAO desconocido: {dao_type}")
        return dao_class

    @classmethod
    def get_usuario_dao(cls):
        """Obtener UsuarioDAO"""
        return cls.create_dao('usuario')

    @classmethod
    def get_evento_dao(cls):
        """Obtener EventoDAO"""
        return cls.create_dao('evento')

    @classmethod
    def get_producto_dao(cls):
        """Obtener ProductoDAO"""
        return cls.create_dao('producto')

    @classmethod
    def get_reserva_dao(cls):
        """Obtener ReservaDAO"""
        return cls.create_dao('reserva')

    @classmethod
    def get_reserva_espacio_dao(cls):
        """Obtener ReservaEspacioDAO"""
        return cls.create_dao('reserva_espacio')
