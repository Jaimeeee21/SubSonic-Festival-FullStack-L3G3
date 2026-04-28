"""
app/routes/auth.py - Autenticación con Firebase
"""
from fastapi import APIRouter, HTTPException, status, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.auth import verify_firebase_token
from app.utils.firebase import get_firestore
from app.utils.database import get_db
from app.DTOs.auth_dto import LoginResponse, VerifyTokenResponse
from app.dao.empresa_dao import EmpresaDAO
from app.models import Usuario, Empresa
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

# Clave secreta para generar tokens JWT locales
SECRET_KEY = "tu-clave-secreta-muy-segura-para-jwt-2024"
ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    token: str


class LoginEmailRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class LoginResponse(BaseModel):
    user_id: str
    success: bool
    message: str


def hash_password(password: str) -> str:
    """Hash una contraseña con salt"""
    salt = secrets.token_hex(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${password_hash.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica una contraseña contra su hash"""
    try:
        salt, stored_hash = password_hash.split('$')
        password_verification = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_verification.hex() == stored_hash
    except:
        return False


def create_jwt_token(user_id: str, expires_delta: timedelta = None):
    """Crea un token JWT"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    
    payload = {
        'user_id': user_id,
        'exp': expire,
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def set_auth_cookies(response: JSONResponse, token: str, user_data: dict, expires_days: int = 7):
    """Agrega cookies seguras a la respuesta HTTP"""
    max_age = expires_days * 24 * 60 * 60  # Convertir días a segundos
    
    # Cookie principal: Token de autenticación
    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=max_age,
        httponly=True,  # No accesible desde JavaScript (protege XSS)
        secure=False,   # Cambiar a True en producción con HTTPS
        samesite="lax"  # Protección contra CSRF
    )
    
    # Cookies adicionales (sin httponly para que JS pueda leerlas para UI)
    for key, value in user_data.items():
        if isinstance(value, str):
            response.set_cookie(
                key=f"user_{key}",
                value=value,
                max_age=max_age,
                httponly=False,  # Accesible desde JS
                secure=False,    # Cambiar a True en producción
                samesite="lax"
            )


@router.post("/login-email-business")
def login_email_business(login_data: LoginEmailRequest, db: Session = Depends(get_db)):
    """
    Login con email para empresas
    Para empresas registradas automáticamente, solo requiere email
    Retorna un token JWT y información de la empresa
    """
    try:
        email = login_data.email.strip().lower()

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email es requerido"
            )

        # Buscar usuario por email EN BD SQL
        usuario = db.query(Usuario).filter(Usuario.email == email).first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No existe cuenta de empresa con este email"
            )

        # Verificar que sea empresa
        if not usuario.es_empresa:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta cuenta no es una cuenta de empresa. Por favor usa el login regular."
            )

        # Obtener empresa asociada
        empresa = db.query(Empresa).filter(Empresa.usuario_id == usuario.id).first()

        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa asociada no encontrada"
            )

        if empresa.estado != "activa":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Empresa {empresa.estado}. Contacta con administración."
            )

        # Crear token JWT
        token = create_jwt_token(str(usuario.id))

        # Preparar datos de usuario para cookies
        user_data = {
            "empresa_nombre": empresa.nombre,
            "usuario_id": str(usuario.id),
            "empresa_id": str(empresa.id),
            "email": usuario.email
        }
        
        # Crear respuesta JSON
        response_data = {
            "success": True,
            "message": f"¡Bienvenido {empresa.nombre}!",
            "token": token,
            "usuario_id": usuario.id,
            "usuario_nombre": usuario.nombre,
            "es_empresa": True,
            "empresa_id": empresa.id,
            "empresa_nombre": empresa.nombre,
            "email": usuario.email
        }
        
        response = JSONResponse(content=response_data)
        set_auth_cookies(response, token, user_data)
        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error en login-email-business: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en login: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Recibe un token de Google y lo verifica con Firebase
    Guarda el usuario en Firestore si no existe
    Usa el email como identificador único
    Retorna el user_id y si es empresa
    """
    try:
        # Verificar el token
        verify_firebase_token(login_data.token)
        
        # Decodificar para obtener información del usuario
        token_info = decode_google_token(login_data.token)
        
        if not token_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo decodificar el token"
            )
        
        # Usar email como identificador único
        email = token_info.get('email', '')
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El token no contiene un email válido"
            )
        
        user_id = email
        db_firestore = get_firestore()
        usuarios_ref = db_firestore.collection('usuarios')
        
        # Verificar si el usuario ya existe
        user_doc = usuarios_ref.document(user_id).get()
        
        es_empresa = False
        empresa_id = None
        
        if not user_doc.exists:
            # Crear nuevo usuario con información de Google
            from datetime import datetime
            usuarios_ref.document(user_id).set({
                'email': email,
                'nombre': token_info.get('name', 'Usuario'),
                'picture': token_info.get('picture', None),
                'tipo_auth': 'google',
                'created_at': datetime.now(),
                'sub': token_info.get('sub'),
                'entradas_compradas': [],
                'es_empresa': False
            })
        else:
            # Verificar si existe empresa asociada en BD SQL
            # Buscar usuario por email en BD SQL
            from app.models import Usuario
            usuario_sql = db.query(Usuario).filter(Usuario.email == email).first()
            if usuario_sql:
                # Verificar si tiene empresa
                try:
                    empresa = EmpresaDAO.obtener_empresa_por_usuario(db, usuario_sql.id)
                    es_empresa = True
                    empresa_id = empresa.id
                except:
                    es_empresa = False
        
        return LoginResponse(
            user_id=user_id,
            success=True,
            message="Autenticación exitosa",
            es_empresa=es_empresa,
            empresa_id=empresa_id
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en autenticación: {str(e)}"
        )


@router.post("/verify")
def verify_token(authorization: str = Header(None)):
    """
    Verifica si el token actual es válido
    Retorna el user_id si es válido
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado"
        )
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de Authorization inválido"
        )
    
    try:
        user_id = verify_firebase_token(parts[1])
        return {
            "valid": True,
            "user_id": user_id,
            "message": "Token válido"
        }
    except HTTPException as e:
        raise e


@router.post("/register", response_model=LoginResponse)
def register(register_data: RegisterRequest):
    """
    Registra un nuevo usuario en Firestore
    Usa el email como identificador único
    Guarda: email, nombre, contraseña hasheada, fecha creación, entradas compradas
    """
    try:
        db = get_firestore()
        
        # Verificar si el usuario ya existe por email
        usuarios_ref = db.collection('usuarios')
        existing = usuarios_ref.where('email', '==', register_data.email).stream()
        
        if list(existing):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email ya está registrado"
            )
        
        # Usar email como user_id
        user_id = register_data.email
        password_hash = hash_password(register_data.password)
        
        from datetime import datetime
        usuarios_ref.document(user_id).set({
            'email': register_data.email,
            'nombre': register_data.name,
            'password_hash': password_hash,
            'tipo_auth': 'email',
            'created_at': datetime.now(),
            'entradas_compradas': []
        })
        
        return LoginResponse(
            user_id=user_id,
            success=True,
            message="Usuario registrado exitosamente"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en registro: {str(e)}"
        )


@router.post("/login-email-client", response_model=LoginResponse)
def login_email_client(login_data: LoginEmailRequest):
    """
    Login tradicional con email y contraseña para CLIENTES
    Verifica contra Firestore que el usuario NO sea empresa
    """
    try:
        db = get_firestore()

        # Buscar usuario por email
        usuarios_ref = db.collection('usuarios')
        user_docs = list(usuarios_ref.where('email', '==', login_data.email).stream())

        if not user_docs:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        user_doc = user_docs[0]
        user_data = user_doc.to_dict()

        # Verificar que NO sea empresa
        if user_data.get('es_empresa', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta cuenta es de empresa. Por favor usa el login de empresa."
            )

        # Verificar contraseña
        if not verify_password(login_data.password, user_data.get('password_hash', '')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        return LoginResponse(
            user_id=user_doc.id,
            success=True,
            message="Login exitoso"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error en login: {str(e)}"
        )


@router.post("/logout")
def logout():
    """
    Logout - limpia las cookies de autenticación
    Se llama desde el frontend
    """
    response = JSONResponse(content={
        "success": True,
        "message": "Sesión cerrada correctamente"
    })
    
    # Limpiar cookies (establecer max_age = 0)
    cookies_to_clear = [
        'auth_token',
        'user_empresa_nombre',
        'user_usuario_id',
        'user_empresa_id',
        'user_email',
        'user_nombre'
    ]
    
    for cookie_name in cookies_to_clear:
        response.delete_cookie(
            key=cookie_name,
            path='/',
            secure=False,  # Cambiar a True en producción con HTTPS
            httponly=True
        )
    
    return response
