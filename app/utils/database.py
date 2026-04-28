from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.utils.firebase import get_firestore, init_firebase

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./test.db"  # Base de datos SQLite local para desarrollo
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Obtener sesión de base de datos SQLAlchemy"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Firestore client
firestore_db = None

def get_firestore_db():
    """Obtener cliente de Firestore"""
    global firestore_db
    if firestore_db is None:
        firestore_db = get_firestore()
    return firestore_db

def init_db():
    """Inicializar Firebase y SQLAlchemy"""
    global firestore_db
    init_firebase()
    firestore_db = get_firestore()
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("[OK] Firestore inicializado correctamente")
    print("[OK] SQLAlchemy inicializado correctamente")
