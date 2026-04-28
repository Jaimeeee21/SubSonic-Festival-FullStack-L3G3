from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Empresa
from app.DTOs.empresa_dto import EmpresaCreate, EmpresaUpdate
from app.utils.exceptions import DatabaseException, SubSonicException


class EmpresaDAO:
    """Data Access Object for Empresa"""

    @staticmethod
    def crear_empresa(db: Session, empresa_data: EmpresaCreate) -> Empresa:
        """Create a new empresa"""
        try:
            nueva_empresa = Empresa(**empresa_data.dict())
            db.add(nueva_empresa)
            db.commit()
            db.refresh(nueva_empresa)
            return nueva_empresa
        except IntegrityError as e:
            db.rollback()
            if "cif" in str(e):
                raise SubSonicException(f"El CIF {empresa_data.cif} ya está registrado")
            raise DatabaseException(f"Error al crear empresa: {str(e)}")
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error al crear empresa: {str(e)}")

    @staticmethod
    def obtener_empresa(db: Session, empresa_id: int) -> Empresa:
        """Get empresa by ID"""
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa:
            raise SubSonicException(f"Empresa no encontrada con ID {empresa_id}")
        return empresa

    @staticmethod
    def obtener_empresa_por_usuario(db: Session, usuario_id: int) -> Empresa:
        """Get empresa by usuario_id"""
        empresa = db.query(Empresa).filter(Empresa.usuario_id == usuario_id).first()
        if not empresa:
            raise SubSonicException(f"No hay empresa registrada para este usuario")
        return empresa

    @staticmethod
    def obtener_empresa_por_cif(db: Session, cif: str) -> Empresa:
        """Get empresa by CIF"""
        empresa = db.query(Empresa).filter(Empresa.cif == cif).first()
        if not empresa:
            raise SubSonicException(f"Empresa no encontrada con CIF {cif}")
        return empresa

    @staticmethod
    def obtener_todas_empresas(db: Session, skip: int = 0, limit: int = 100) -> list[Empresa]:
        """Get all empresas"""
        return db.query(Empresa).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_empresas_por_tipo(db: Session, tipo_empresa: str) -> list[Empresa]:
        """Get empresas by tipo"""
        return db.query(Empresa).filter(Empresa.tipo_empresa == tipo_empresa).all()

    @staticmethod
    def obtener_empresas_activas(db: Session) -> list[Empresa]:
        """Get all active empresas"""
        return db.query(Empresa).filter(Empresa.estado == "activa").all()

    @staticmethod
    def actualizar_empresa(db: Session, empresa_id: int, empresa_update: EmpresaUpdate) -> Empresa:
        """Update empresa"""
        try:
            empresa = EmpresaDAO.obtener_empresa(db, empresa_id)
            update_data = empresa_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(empresa, field, value)
            db.commit()
            db.refresh(empresa)
            return empresa
        except IntegrityError as e:
            db.rollback()
            if "cif" in str(e):
                raise SubSonicException(f"El CIF ya está registrado")
            raise DatabaseException(f"Error al actualizar empresa: {str(e)}")
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error al actualizar empresa: {str(e)}")

    @staticmethod
    def eliminar_empresa(db: Session, empresa_id: int) -> dict:
        """Delete empresa"""
        try:
            empresa = EmpresaDAO.obtener_empresa(db, empresa_id)
            db.delete(empresa)
            db.commit()
            return {"message": f"Empresa eliminada correctamente"}
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error al eliminar empresa: {str(e)}")

    @staticmethod
    def cambiar_estado_empresa(db: Session, empresa_id: int, nuevo_estado: str) -> Empresa:
        """Change empresa state"""
        try:
            empresa = EmpresaDAO.obtener_empresa(db, empresa_id)
            empresa.estado = nuevo_estado
            db.commit()
            db.refresh(empresa)
            return empresa
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error al cambiar estado: {str(e)}")
