from fastapi import APIRouter, HTTPException, status, Header, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
from app.services.empresa_service import EmpresaService
from app.DTOs.empresa_dto import EmpresaCreate, EmpresaUpdate, EmpresaResponse, EmpresaPanelResponse
from app.utils.exceptions import SubSonicException
from app.utils.auth import get_user_from_token
from app.utils.database import get_db
from app.utils.firebase import get_firestore
from app.models import Usuario, Empresa
from datetime import datetime
import hashlib
import secrets
import uuid

router = APIRouter(prefix="/api/empresas", tags=["Empresas"])


class RegistroEmpresaRequest(BaseModel):
    """Schema para registro de nueva empresa"""
    nombre: str
    cif: str
    tipo_empresa: str
    descripcion: str
    telefono: str
    email_contacto: str
    website: Optional[str] = None
    logo_url: Optional[str] = None


@router.post("/registro", response_model=dict, status_code=status.HTTP_201_CREATED)
def registrar_empresa(data: RegistroEmpresaRequest, db: Session = Depends(get_db)):
    """
    Registrar una nueva empresa
    Crea automáticamente un usuario con email de empresa
    Guarda en SQL y TAMBIÉN en Firestore
    """
    try:
        # Verificar que el email no existe
        usuario_existente = db.query(Usuario).filter(Usuario.email == data.email_contacto).first()
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email ya está registrado"
            )
        
        # Verificar que el CIF no existe
        empresa_existente = db.query(Empresa).filter(Empresa.cif == data.cif).first()
        if empresa_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este CIF ya está registrado"
            )
        
        # Crear usuario empresa
        usuario = Usuario(
            nombre=data.nombre,
            email=data.email_contacto,
            password=secrets.token_hex(16),  # Contraseña temporal
            es_empresa=True,
            empresa_nombre=data.nombre,
            empresa_cif=data.cif
        )
        
        db.add(usuario)
        db.flush()  # Para obtener el ID
        
        # Crear empresa en SQL
        empresa = Empresa(
            usuario_id=usuario.id,
            nombre=data.nombre,
            cif=data.cif,
            descripcion=data.descripcion,
            telefono=data.telefono,
            email_contacto=data.email_contacto,
            website=data.website,
            logo_url=data.logo_url,
            tipo_empresa=data.tipo_empresa,
            estado="activa"
        )
        
        db.add(empresa)
        db.commit()
        db.refresh(empresa)
        
        # GUARDAR TAMBIÉN EN FIRESTORE
        try:
            firestore_db = get_firestore()
            empresa_id = str(uuid.uuid4())

            empresa_firestore = {
                'id': empresa_id,
                'usuario_id': usuario.id,
                'nombre': data.nombre,
                'cif': data.cif,
                'tipo_empresa': data.tipo_empresa,
                'descripcion': data.descripcion,
                'telefono': data.telefono,
                'email_contacto': data.email_contacto,
                'website': data.website or '',
                'logo_url': data.logo_url or '',
                'estado': 'activa',
                'fecha_registro': datetime.utcnow().isoformat()
            }

            # Guardar empresa en colección "empresas"
            firestore_db.collection('empresas').document(empresa_id).set(empresa_firestore)
            print(f"✅ Empresa guardada en Firestore: {empresa_id}")

            # IMPORTANTE: También guardar el usuario en Firestore (para que pueda acceder a su perfil)
            usuario_firestore = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.email,
                'es_empresa': True,
                'empresa_id': empresa_id,
                'empresa_nombre': data.nombre,
                'empresa_cif': data.cif,
                'tipo_empresa': data.tipo_empresa,
                'created_at': datetime.utcnow().isoformat()
            }
            firestore_db.collection('usuarios').document(usuario.id).set(usuario_firestore)
            print(f"✅ Usuario empresa guardado en Firestore: {usuario.id}")

        except Exception as firebase_error:
            print(f"⚠️ Advertencia: No se pudo guardar en Firestore: {str(firebase_error)}")
            # No lanzar excepción, ya que la empresa se guardó en SQL
        
        return {
            "success": True,
            "message": "Empresa registrada exitosamente",
            "empresa_id": empresa.id,
            "usuario_id": usuario.id,
            "email": usuario.email,
            "nombre": empresa.nombre
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en registro: {str(e)}"
        )


@router.post("", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def crear_empresa(empresa: EmpresaCreate, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Crear una nueva empresa (requiere autenticación)"""
    try:
        user_id = get_user_from_token(authorization)
        return EmpresaService.crear_empresa(empresa, db, user_id=user_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener datos de una empresa"""
    try:
        return EmpresaService.obtener_empresa(empresa_id, db)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=list[EmpresaResponse])
def obtener_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las empresas"""
    try:
        return EmpresaService.obtener_todas_empresas(db, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/usuario/panel", response_model=EmpresaPanelResponse)
def obtener_panel_empresa(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Obtener panel de empresa del usuario autenticado (con espacios reservados)"""
    try:
        user_id = get_user_from_token(authorization)
        return EmpresaService.obtener_panel_empresa(user_id, db)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/usuario/mi-empresa", response_model=EmpresaResponse)
def obtener_mi_empresa(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Obtener datos de la empresa del usuario autenticado"""
    try:
        user_id = get_user_from_token(authorization)
        return EmpresaService.obtener_empresa_usuario(user_id, db)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def actualizar_empresa(empresa_id: int, empresa_update: EmpresaUpdate, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Actualizar datos de empresa (requiere autenticación)"""
    try:
        user_id = get_user_from_token(authorization)
        return EmpresaService.actualizar_empresa(empresa_id, empresa_update, db)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{empresa_id}")
def eliminar_empresa(empresa_id: int, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Eliminar una empresa (requiere autenticación)"""
    try:
        user_id = get_user_from_token(authorization)
        return EmpresaService.eliminar_empresa(empresa_id, db)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{empresa_id}/estado")
def cambiar_estado(empresa_id: int, nuevo_estado: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Cambiar estado de empresa (activa, inactiva, suspendida)"""
    try:
        user_id = get_user_from_token(authorization)
        return EmpresaService.cambiar_estado(empresa_id, nuevo_estado, db)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/firebase/todas")
def obtener_empresas_firestore():
    """
    Obtener TODAS las empresas desde Firestore
    Útil para verificar que las empresas se guardan correctamente
    """
    try:
        firestore_db = get_firestore()
        docs = firestore_db.collection('empresas').stream()
        
        empresas = []
        for doc in docs:
            empresa = doc.to_dict()
            empresas.append(empresa)
        
        print(f"✅ Cargadas {len(empresas)} empresas desde Firestore")
        return {
            "success": True,
            "total": len(empresas),
            "empresas": empresas
        }
    except Exception as e:
        print(f"❌ Error al obtener empresas de Firestore: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener empresas: {str(e)}"
        )
