#!/usr/bin/env python3
"""
Script RÁPIDO para poblar Firestore sin cuelgues
Inserta datos directamente sin esperas
"""
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from pathlib import Path

# Inicializar Firebase
cred_path = Path(__file__).parent / "subsonic-festival-56216-3767f772323c.json"
print(f"Buscando credenciales en: {cred_path}")

if not cred_path.exists():
    print(f"❌ NO ENCONTRADO: {cred_path}")
    exit(1)

try:
    cred = credentials.Certificate(str(cred_path))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase inicializado\n")
except Exception as e:
    print(f"❌ Error inicializando Firebase: {e}")
    exit(1)

# Preparar datos
print("📋 Preparando datos...")

eventos = {
    "madrid": {"id": "madrid", "title": "SUBSONIC 2026", "date": "15-17 Agosto", "location": "Madrid", "description": "La experiencia musical más electrizante del año en Madrid. 50,000+ asistentes, 3 escenarios simultáneos", "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop", "info": ["📅 15-17 de Agosto", "📍 Madrid, España"], "artists": {"Escenario 1": ["The Sonic Masters", "Luna Sky", "Rhythm & Beats", "Urban Beats"], "Escenario 2": ["Electric Horizon", "Deep Groove Collective", "Cyber Pulse", "Jazz Collective", "Classical Chaos"], "Escenario 3": ["Melodic Echoes", "Neon Pulse", "Solar Waves", "Sonic Velocity", "Neon Dream"]}, "capacidad": 50000, "created_at": datetime.now(), "updated_at": datetime.now()},
    "barcelona": {"id": "barcelona", "title": "SUBSONIC 2026", "date": "22-24 Agosto", "location": "Barcelona", "description": "La experiencia musical más electrizante del año en Barcelona. 50,000+ asistentes, 3 escenarios simultáneos", "image": "https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=400&h=300&fit=crop", "info": ["📅 22-24 de Agosto", "📍 Barcelona, España"], "artists": {"Escenario 1": ["Melodic Echoes", "The Sonic Masters", "Rhythm & Beats", "Sonic Waves", "Sonic Velocity", "Luna Sky"], "Escenario 2": ["Deep Groove Collective", "Electric Horizon", "Cyber Pulse", "Urban Beats", "Classical Chaos"], "Escenario 3": ["Luna Sky", "Neon Pulse", "Solar Waves", "Jazz Collective", "Neon Dream"]}, "capacidad": 50000, "created_at": datetime.now(), "updated_at": datetime.now()},
    "valencia": {"id": "valencia", "title": "SUBSONIC 2026", "date": "29-31 Agosto", "location": "Valencia", "description": "La experiencia musical más electrizante del año en Valencia. 50,000+ asistentes, 3 escenarios simultáneos", "image": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=400&h=300&fit=crop", "info": ["📅 29-31 de Agosto", "📍 Valencia, España"], "artists": {"Escenario 1": ["The Sonic Masters", "Luna Sky", "Rhythm & Beats", "Urban Beats", "Sonic Waves"], "Escenario 2": ["Electric Horizon", "Deep Groove Collective", "Cyber Pulse", "Jazz Collective", "Classical Chaos"], "Escenario 3": ["Melodic Echoes", "Neon Pulse", "Solar Waves", "Sonic Velocity", "Neon Dream"]}, "capacidad": 50000, "created_at": datetime.now(), "updated_at": datetime.now()},
    "bilbao": {"id": "bilbao", "title": "SUBSONIC 2026", "date": "5-7 Septiembre", "location": "Bilbao", "description": "La experiencia musical más electrizante del año en Bilbao. 50,000+ asistentes, 3 escenarios simultáneos", "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&h=300&fit=crop", "info": ["📅 5-7 de Septiembre", "📍 Bilbao, España"], "artists": {"Escenario 1": ["The Sonic Masters", "Luna Sky", "Rhythm & Beats", "Urban Beats", "Sonic Waves"], "Escenario 2": ["Electric Horizon", "Deep Groove Collective", "Cyber Pulse", "Jazz Collective", "Classical Chaos"], "Escenario 3": ["Melodic Echoes", "Neon Pulse", "Solar Waves", "Sonic Velocity", "Neon Dream"]}, "capacidad": 50000, "created_at": datetime.now(), "updated_at": datetime.now()},
    "sevilla": {"id": "sevilla", "title": "SUBSONIC 2026", "date": "12-14 Septiembre", "location": "Sevilla", "description": "El festival más esperado del año en Andalucía. Más de 60,000 festivaleros", "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop", "info": ["📅 12-14 de Septiembre", "📍 Sevilla, España"], "artists": {"Escenario 1": ["Deep Groove Collective", "The Sonic Masters", "Solar Waves", "Rhythm & Beats", "Sonic Waves", "Luna Sky"], "Escenario 2": ["Electric Horizon", "Luna Sky", "Cyber Pulse", "Jazz Collective", "Neon Pulse"], "Escenario 3": ["Melodic Echoes", "Urban Beats", "Sonic Velocity", "Neon Dream", "Classical Chaos"]}, "capacidad": 60000, "created_at": datetime.now(), "updated_at": datetime.now()},
    "malaga": {"id": "malaga", "title": "SUBSONIC 2026", "date": "19-21 Septiembre", "location": "Málaga", "description": "La experiencia musical más electrizante del año en Costa del Sol. 50,000+ asistentes", "image": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=400&h=300&fit=crop", "info": ["📅 19-21 de Septiembre", "📍 Málaga, España"], "artists": {"Escenario 1": ["The Sonic Masters", "Luna Sky", "Rhythm & Beats", "Sonic Waves", "Urban Beats"], "Escenario 2": ["Deep Groove Collective", "Electric Horizon", "Jazz Collective", "Cyber Pulse"], "Escenario 3": ["Melodic Echoes", "Solar Waves", "Neon Pulse", "Sonic Velocity", "Neon Dream"]}, "capacidad": 50000, "created_at": datetime.now(), "updated_at": datetime.now()}
}

productos = [
    {"id": "camiseta-classic", "name": "Camiseta SUBSONIC Classic", "description": "Tela de 100% algodón con logo bordado", "price": "$29.99", "category": "ropa", "colores": ["Negro", "Blanco", "Azul Neon"], "stock": 100},
    {"id": "sudadera-subsonic", "name": "Hoodie SUBSONIC", "description": "Sudadera premium con capucha ajustable", "price": "$49.99", "category": "ropa", "colores": ["Negro", "Gris Oscuro", "Purpura"], "stock": 75},
    {"id": "pantalones-jogger", "name": "Pantalones SUBSONIC Jogger", "description": "Comodidad total con diseño moderno", "price": "$39.99", "category": "ropa", "colores": ["Negro", "Gris"], "stock": 60},
    {"id": "gorra-trucker", "name": "Gorra SUBSONIC Trucker", "description": "Gorra ajustable con malla trasera", "price": "$19.99", "category": "accesorios", "colores": ["Negro", "Azul"], "stock": 200},
    {"id": "botella-hydro", "name": "Botella SUBSONIC Hydro", "description": "Térmica deportiva con logo grabado", "price": "$24.99", "category": "accesorios", "colores": ["Negro", "Plateado"], "stock": 150},
    {"id": "pulsera-led", "name": "Pulsera SUBSONIC LED", "description": "Pulsera LED interactiva para festivales", "price": "$14.99", "category": "accesorios", "colores": ["Azul Neon", "Rosa Neon"], "stock": 300}
]

usuarios = [
    {"id": "user_juan", "nombre": "Juan Pérez", "email": "juan@example.com", "created_at": datetime.now()},
    {"id": "user_admin", "nombre": "Admin SubSonic", "email": "admin@subsonic.com", "created_at": datetime.now()}
]

artistas = [
    {"id": "sonic-masters", "nombre": "The Sonic Masters", "genero": "Electronic / Techno"},
    {"id": "luna-sky", "nombre": "Luna Sky", "genero": "Ambient / Chill"},
    {"id": "rhythm-beats", "nombre": "Rhythm & Beats", "genero": "Hip-Hop / Rap"},
    {"id": "urban-beats", "nombre": "Urban Beats", "genero": "Reggaeton / Trap"},
    {"id": "electric-horizon", "nombre": "Electric Horizon", "genero": "Rock/Indie"},
    {"id": "deep-groove", "nombre": "Deep Groove Collective", "genero": "House / Funk"},
    {"id": "cyber-pulse", "nombre": "Cyber Pulse", "genero": "Experimental"},
    {"id": "jazz-collective", "nombre": "Jazz Collective", "genero": "Jazz / Fusion"},
    {"id": "melodic-echoes", "nombre": "Melodic Echoes", "genero": "Indie / Alternative"},
    {"id": "neon-pulse", "nombre": "Neon Pulse", "genero": "Synthwave / Electro"},
    {"id": "solar-waves", "nombre": "Solar Waves", "genero": "House / Electronic"},
    {"id": "sonic-velocity", "nombre": "Sonic Velocity", "genero": "Electronic / Trance"},
    {"id": "neon-dream", "nombre": "Neon Dream", "genero": "Synthwave / Electro"},
    {"id": "classical-chaos", "nombre": "Classical Chaos", "genero": "Orquesta / Electrónica"}
]

categorias = [
    {"id": "ropa", "nombre": "Ropa", "descripcion": "Prendas y ropa SUBSONIC"},
    {"id": "accesorios", "nombre": "Accesorios", "descripcion": "Accesorios y complementos"},
    {"id": "edicion-limitada", "nombre": "Edición Limitada", "descripcion": "Artículos de edición limitada"}
]

# INSERTAR DIRECTAMENTE
print("🔥 Insertando AHORA (sin esperas)...\n")

try:
    print("📅 Eventos:", end=" ")
    for evento_id, evento_data in eventos.items():
        db.collection("eventos").document(evento_id).set(evento_data)
    print(f"✅ {len(eventos)}")
    
    print("🛍️  Productos:", end=" ")
    for producto in productos:
        db.collection("productos").document(producto["id"]).set(producto)
    print(f"✅ {len(productos)}")
    
    print("👥 Usuarios:", end=" ")
    for usuario in usuarios:
        db.collection("usuarios").document(usuario["id"]).set(usuario)
    print(f"✅ {len(usuarios)}")
    
    print("🎤 Artistas:", end=" ")
    for artista in artistas:
        db.collection("artistas").document(artista["id"]).set(artista)
    print(f"✅ {len(artistas)}")
    
    print("📂 Categorías:", end=" ")
    for categoria in categorias:
        db.collection("categorias").document(categoria["id"]).set(categoria)
    print(f"✅ {len(categorias)}")
    
    print("\n" + "="*50)
    print("✅ ¡INSERCIÓN COMPLETADA!")
    print("="*50)
    print(f"📊 TOTAL: {len(eventos) + len(productos) + len(usuarios) + len(artistas) + len(categorias)} documentos")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
