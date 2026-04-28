from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils.database import Base


class Usuario(Base):
    """Usuario model - Personas y Empresas"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    es_empresa = Column(Boolean, default=False)
    empresa_nombre = Column(String(255), nullable=True)
    empresa_cif = Column(String(20), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")
    reservas_espacios = relationship("ReservaEspacio", back_populates="usuario", cascade="all, delete-orphan")


class Evento(Base):
    """Evento model - Eventos del festival"""
    __tablename__ = "eventos"

    id = Column(String(100), primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    fecha = Column(String(100), nullable=False)  # ej: "15-17 Agosto"
    ubicacion = Column(String(255), nullable=False)
    imagen_url = Column(String(500))
    capacidad = Column(Integer)
    artistas = Column(JSON)  # Almacenar array de artistas con sus horarios y escenarios
    info = Column(JSON)  # Array de info adicional
    espacios_disponibles = Column(JSON)  # Array de espacios disponibles para reservar (food-trucks, stalls, booths)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservas = relationship("Reserva", back_populates="evento", cascade="all, delete-orphan")


class Producto(Base):
    """Producto model - Merchandising"""
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    categoria = Column(String(100), nullable=False)  # ropa, accesorios, edicion-limitada
    imagen_default = Column(String(500))
    colores = Column(JSON)  # Array de colores con hex, imagen, etc
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items_carrito = relationship("ItemCarrito", back_populates="producto", cascade="all, delete-orphan")


class ItemCarrito(Base):
    """ItemCarrito model - Items en carrito de compra"""
    __tablename__ = "items_carrito"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cantidad = Column(Integer, default=1)
    talla = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    producto = relationship("Producto", back_populates="items_carrito")


class Reserva(Base):
    """Reserva model - Reserva de tickets para eventos"""
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    evento_id = Column(String(100), ForeignKey("eventos.id"), nullable=False)
    cantidad_entradas = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)
    estado = Column(String(50), default="pendiente")  # pendiente, confirmada, cancelada
    fecha_reserva = Column(DateTime, default=datetime.utcnow)
    fecha_evento = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    usuario = relationship("Usuario", back_populates="reservas")
    evento = relationship("Evento", back_populates="reservas")


class ReservaEspacio(Base):
    """ReservaEspacio model - Reserva de espacios para food trucks y empresas"""
    __tablename__ = "reservas_espacios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    evento_id = Column(String(100), ForeignKey("eventos.id"), nullable=True)  # Evento donde se reserva
    espacio_id = Column(String(100), nullable=False)  # ID del espacio (para tracking)
    tipo_espacio = Column(String(50), nullable=False)  # food-truck, stall, booth, popup-store
    nombre_espacio = Column(String(255), nullable=False)
    tamaño = Column(String(50), nullable=False)  # ej: "3m × 6m"
    descripcion = Column(Text)
    nombre_negocio = Column(String(255), nullable=False)
    precio = Column(Float, nullable=False)
    estado = Column(String(50), default="pendiente")  # pendiente, confirmada, cancelada, disponible
    fecha_reserva = Column(DateTime, default=datetime.utcnow)
    ubicacion_ideales = Column(JSON)  # Array de ubicaciones preferidas
    servicios_requiere = Column(JSON)  # Array de servicios necesarios
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    usuario = relationship("Usuario", back_populates="reservas_espacios")
    evento = relationship("Evento", backref="reservas_espacios")


class Empresa(Base):
    """Empresa model - Empresas registradas para espacios en el festival"""
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, unique=True)
    nombre = Column(String(255), nullable=False)
    cif = Column(String(20), nullable=False, unique=True, index=True)
    descripcion = Column(Text)
    telefono = Column(String(20), nullable=False)
    email_contacto = Column(String(255), nullable=False)
    website = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    tipo_empresa = Column(String(100), nullable=False)  # food-truck, catering, merchandising, sponsor, etc
    estado = Column(String(50), default="activa")  # activa, inactiva, suspendida
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    espacios_reservados = relationship("ReservaEspacio", primaryjoin="Empresa.usuario_id == ReservaEspacio.usuario_id", foreign_keys="ReservaEspacio.usuario_id", viewonly=True)
