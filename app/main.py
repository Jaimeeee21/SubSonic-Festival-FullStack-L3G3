from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from app.utils.firebase import init_firebase
from app.utils.database import init_db
from app.routes import usuarios, eventos, productos, reservas, espacios, auth, empresa, reserva_espacios
from app.utils.exceptions import SubSonicException

def create_app():
    """Crear y configurar la aplicación FastAPI"""
    
    # Inicializar base de datos y Firebase
    try:
        init_db()
        print("[OK] Base de datos SQLAlchemy inicializada correctamente")
    except Exception as e:
        print(f"[ERROR] Base de datos initialization error: {str(e)}")
        raise
    
    # Crear instancia de FastAPI
    app = FastAPI(
        title="SubSonic Festival API",
        description="API para el festival SubSonic - Gestión de eventos, merchandising y reservas",
        version="1.0.0"
    )
    
    # Configurar CORS para permitir requests desde el frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://pil3g3.duckdns.org", "http://localhost:3000", "http://localhost:5500", "*"],  # En producción especificar dominio
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar rutas de API
    app.include_router(auth.router)
    app.include_router(usuarios.router)
    app.include_router(eventos.router)
    app.include_router(productos.router)
    app.include_router(reservas.router)
    app.include_router(espacios.router)
    app.include_router(empresa.router)
    app.include_router(reserva_espacios.router)
    
    # Servir archivos estáticos del frontend
    frontend_path = Path(__file__).parent.parent / "public"
    if frontend_path.exists():
        app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    # Ruta raíz que sirve el index.html
    @app.get("/")
    async def root():
        index_path = frontend_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"message": "SubSonic Festival API - Abre http://pil3g3.duckdns.org/docs para la documentación"}
    
    # Rutas para servir directamente archivos HTML del frontend
    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str):
        # Evitar servir archivos de API
        if file_path.startswith("api/"):
            return HTTPException(status_code=404)
        
        # Intentar servir archivos estáticos del frontend
        file_full_path = frontend_path / file_path
        
        # Validar que la ruta está dentro de frontend_path (seguridad)
        try:
            file_full_path.resolve().relative_to(frontend_path.resolve())
        except ValueError:
            return HTTPException(status_code=403, detail="Acceso denegado")
        
        if file_full_path.exists() and file_full_path.is_file():
            return FileResponse(file_full_path)
        
        # Si no es archivo, intentar servir index.html (para rutas frontend)
        index_path = frontend_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        return HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Exception handlers
    @app.exception_handler(SubSonicException)
    async def subsonic_exception_handler(request, exc):
        return HTTPException(status_code=400, detail=str(exc))
    
    # Health check
    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    return app

# Crear la aplicación
app = create_app()
