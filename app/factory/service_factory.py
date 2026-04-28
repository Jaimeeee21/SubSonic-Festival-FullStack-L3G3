from app.services.usuario_service import UsuarioService
from app.services.evento_service import EventoService
from app.services.producto_service import ProductoService
from app.services.reserva_service import ReservaService
from app.services.reserva_espacio_service import ReservaEspacioService


class ServiceFactory:
    """Factory para crear instancias de Services"""

    _services = {
        'usuario': UsuarioService,
        'evento': EventoService,
        'producto': ProductoService,
        'reserva': ReservaService,
        'reserva_espacio': ReservaEspacioService,
    }

    @classmethod
    def create_service(cls, service_type: str):
        """
        Crear una instancia de Service por tipo
        
        Args:
            service_type: Tipo de servicio a crear
        
        Returns:
            Instancia del servicio solicitado
        """
        service_class = cls._services.get(service_type.lower())
        if not service_class:
            raise ValueError(f"Servicio desconocido: {service_type}")
        return service_class

    @classmethod
    def get_usuario_service(cls):
        """Obtener UsuarioService"""
        return cls.create_service('usuario')

    @classmethod
    def get_evento_service(cls):
        """Obtener EventoService"""
        return cls.create_service('evento')

    @classmethod
    def get_producto_service(cls):
        """Obtener ProductoService"""
        return cls.create_service('producto')

    @classmethod
    def get_reserva_service(cls):
        """Obtener ReservaService"""
        return cls.create_service('reserva')

    @classmethod
    def get_reserva_espacio_service(cls):
        """Obtener ReservaEspacioService"""
        return cls.create_service('reserva_espacio')
