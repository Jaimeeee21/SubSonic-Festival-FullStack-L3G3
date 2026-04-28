from fastapi import APIRouter, HTTPException, status
from app.services.usuario_service import UsuarioService
from app.DTOs.usuario_dto import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin
from app.utils.exceptions import SubSonicException

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate):
    """Registrar un nuevo usuario"""
    try:
        return UsuarioService.registrar_usuario(usuario)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=UsuarioResponse)
def login(credenciales: UsuarioLogin):
    """Login de usuario"""
    try:
        return UsuarioService.login(credenciales.email, credenciales.password)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: str):
    """Obtener datos de un usuario"""
    try:
        return UsuarioService.obtener_usuario(usuario_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[UsuarioResponse])
def obtener_usuarios(skip: int = 0, limit: int = 100):
    """Obtener lista de usuarios"""
    return UsuarioService.obtener_usuarios(skip, limit)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: str, usuario_update: UsuarioUpdate):
    """Actualizar datos de usuario"""
    try:
        return UsuarioService.actualizar_usuario(usuario_id, usuario_update)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: str):
    """Eliminar un usuario"""
    try:
        return UsuarioService.eliminar_usuario(usuario_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/email/{email}", response_model=UsuarioResponse)
def obtener_por_email(email: str):
    """Obtener usuario por email"""
    try:
        return UsuarioService.obtener_por_email(email)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{usuario_id}/perfil")
def obtener_perfil(usuario_id: str):
    """Obtener el perfil completo del usuario con sus entradas compradas"""
    try:
        return UsuarioService.obtener_perfil(usuario_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{usuario_id}/foto-perfil")
def actualizar_foto_perfil(usuario_id: str, foto_url: dict):
    """Actualizar la foto de perfil del usuario"""
    try:
        foto = foto_url.get("foto_perfil") if isinstance(foto_url, dict) else foto_url
        return UsuarioService.actualizar_foto_perfil(usuario_id, foto)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{usuario_id}/entradas-compradas")
def agregar_entrada_comprada(usuario_id: str, entrada: dict):
    """Agregar una entrada comprada al usuario"""
    try:
        return UsuarioService.agregar_entrada_comprada(usuario_id, entrada)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
