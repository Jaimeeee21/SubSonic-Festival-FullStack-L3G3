from sqlalchemy.orm import Session
from app.dao.empresa_dao import EmpresaDAO
from app.DTOs.empresa_dto import EmpresaCreate, EmpresaUpdate, EmpresaResponse, EmpresaPanelResponse
from app.models import ReservaEspacio
from app.utils.exceptions import SubSonicException


class EmpresaService:
    """Service layer for Empresa operations"""

    @staticmethod
    def crear_empresa(empresa_data: EmpresaCreate, db: Session, user_id: int = None) -> EmpresaResponse:
        """Create a new empresa"""
        if user_id:
            empresa_data.usuario_id = user_id
        
        empresa = EmpresaDAO.crear_empresa(db, empresa_data)
        return EmpresaResponse.from_orm(empresa)

    @staticmethod
    def obtener_empresa(empresa_id: int, db: Session) -> EmpresaResponse:
        """Get empresa by ID"""
        empresa = EmpresaDAO.obtener_empresa(db, empresa_id)
        return EmpresaResponse.from_orm(empresa)

    @staticmethod
    def obtener_empresa_usuario(usuario_id: int, db: Session) -> EmpresaResponse:
        """Get empresa for a user"""
        empresa = EmpresaDAO.obtener_empresa_por_usuario(db, usuario_id)
        return EmpresaResponse.from_orm(empresa)

    @staticmethod
    def obtener_panel_empresa(usuario_id: int, db: Session) -> EmpresaPanelResponse:
        """Get empresa panel with reservations"""
        empresa = EmpresaDAO.obtener_empresa_por_usuario(db, usuario_id)
        
        # Get espacios reservados por esta empresa (usuario)
        espacios_reservados = db.query(ReservaEspacio).filter(
            ReservaEspacio.usuario_id == usuario_id
        ).all()
        
        panel_data = {
            "id": empresa.id,
            "nombre": empresa.nombre,
            "cif": empresa.cif,
            "descripcion": empresa.descripcion,
            "telefono": empresa.telefono,
            "email_contacto": empresa.email_contacto,
            "website": empresa.website,
            "logo_url": empresa.logo_url,
            "tipo_empresa": empresa.tipo_empresa,
            "estado": empresa.estado,
            "espacios_reservados": [
                {
                    "id": espacio.id,
                    "tipo_espacio": espacio.tipo_espacio,
                    "nombre_espacio": espacio.nombre_espacio,
                    "tamaño": espacio.tamaño,
                    "descripcion": espacio.descripcion,
                    "nombre_negocio": espacio.nombre_negocio,
                    "precio": espacio.precio,
                    "estado": espacio.estado,
                    "fecha_reserva": espacio.fecha_reserva,
                    "ubicacion_ideales": espacio.ubicacion_ideales,
                    "servicios_requiere": espacio.servicios_requiere
                }
                for espacio in espacios_reservados
            ],
            "created_at": empresa.created_at,
            "updated_at": empresa.updated_at
        }
        
        return EmpresaPanelResponse(**panel_data)

    @staticmethod
    def actualizar_empresa(empresa_id: int, empresa_update: EmpresaUpdate, db: Session) -> EmpresaResponse:
        """Update empresa"""
        empresa = EmpresaDAO.actualizar_empresa(db, empresa_id, empresa_update)
        return EmpresaResponse.from_orm(empresa)

    @staticmethod
    def eliminar_empresa(empresa_id: int, db: Session) -> dict:
        """Delete empresa"""
        return EmpresaDAO.eliminar_empresa(db, empresa_id)

    @staticmethod
    def obtener_todas_empresas(db: Session, skip: int = 0, limit: int = 100) -> list[EmpresaResponse]:
        """Get all empresas"""
        empresas = EmpresaDAO.obtener_todas_empresas(db, skip, limit)
        return [EmpresaResponse.from_orm(e) for e in empresas]

    @staticmethod
    def cambiar_estado(empresa_id: int, nuevo_estado: str, db: Session) -> EmpresaResponse:
        """Change empresa state"""
        empresa = EmpresaDAO.cambiar_estado_empresa(db, empresa_id, nuevo_estado)
        return EmpresaResponse.from_orm(empresa)
