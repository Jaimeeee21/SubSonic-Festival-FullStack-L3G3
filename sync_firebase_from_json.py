#!/usr/bin/env python3
"""
Script para sincronizar Firebase con los datos correctos del JSON del frontend
Actualiza tanto la colección de artistas como la de eventos
"""
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from pathlib import Path
import json

# Función para encontrar credenciales de Firebase automáticamente
def get_firebase_credentials():
    root_dir = Path(__file__).parent
    json_files = list(root_dir.glob("*subsonic*.json"))
    if not json_files:
        json_files = list(root_dir.glob("*.json"))
    if json_files:
        return json_files[0]
    raise FileNotFoundError("No se encontró archivo de credenciales JSON en la carpeta raíz")

# Inicializar Firebase
cred_path = get_firebase_credentials()
print(f"🔍 Buscando credenciales en: {cred_path}")

try:
    cred = credentials.Certificate(str(cred_path))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase inicializado\n")
except Exception as e:
    print(f"❌ Error inicializando Firebase: {e}")
    exit(1)

# Cargar datos del JSON del frontend
json_path = Path(__file__).parent / "public" / "eventos-data.json"
print(f"📂 Leyendo eventos del JSON: {json_path}\n")

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except Exception as e:
    print(f"❌ Error leyendo JSON: {e}")
    exit(1)

# Extraer todos los artistas únicos del JSON
artistas_dict = {}
eventos_data = json_data.get("principales", [])

print("🎤 Extrayendo artistas únicos del JSON...\n")

for evento in eventos_data:
    artists = evento.get("artists", {})
    # artists puede ser un diccionario con escenarios
    if isinstance(artists, dict):
        for escenario, artist_list in artists.items():
            for artist in artist_list:
                artist_id = artist.get("name", "").lower().replace(" ", "-")
                if artist_id not in artistas_dict:
                    artistas_dict[artist_id] = {
                        "id": artist_id,
                        "nombre": artist.get("name", ""),
                        "genero": artist.get("genre", ""),
                        "spotify_url": artist.get("spotify_url", ""),
                        "created_at": datetime.now(),
                        "updated_at": datetime.now()
                    }
                    print(f"  ✓ {artist.get('name')} ({artist.get('genre')})")

print(f"\n📊 Total de artistas únicos: {len(artistas_dict)}\n")

# Limpiar colección de artistas antigua
print("🗑️  Limpiando colección de artistas antigua...")
artistas_ref = db.collection("artistas")
docs = artistas_ref.stream()
count = 0
for doc in docs:
    doc.reference.delete()
    count += 1
print(f"   ✓ Eliminados {count} documentos\n")

# Insertar nuevos artistas
print("📝 Insertando artistas actualizados...")
for artist_id, artist_data in artistas_dict.items():
    db.collection("artistas").document(artist_id).set(artist_data)
    print(f"   ✓ {artist_data['nombre']}")

print(f"\n✅ {len(artistas_dict)} artistas insertados\n")

# Procesar eventos
print("📅 Procesando eventos...\n")

# Limpiar colección de eventos antigua
print("🗑️  Limpiando colección de eventos antigua...")
eventos_ref = db.collection("eventos")
docs = eventos_ref.stream()
count = 0
for doc in docs:
    doc.reference.delete()
    count += 1
print(f"   ✓ Eliminados {count} documentos\n")

# Insertar nuevos eventos con artistas
print("📝 Insertando eventos actualizados...")
for evento in eventos_data:
    evento_id = evento.get("id", "")
    
    # Preparar datos del evento
    evento_doc = {
        "id": evento_id,
        "title": evento.get("title", ""),
        "date": evento.get("date", ""),
        "location": evento.get("location", ""),
        "description": evento.get("description", ""),
        "image": evento.get("image", ""),
        "info": evento.get("info", []),
        "artists": evento.get("artists", {}),  # Estructura completa con escenarios
        "espacios_disponibles": evento.get("espacios_disponibles", []),  # Espacios para reservar
        "capacidad": evento.get("capacidad", 50000),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    db.collection("eventos").document(evento_id).set(evento_doc)
    
    # Contar artistas en el evento
    artists = evento.get("artists", {})
    total_artists = sum(len(v) if isinstance(v, list) else 0 for v in artists.values())
    
    print(f"   ✓ {evento.get('location')} ({evento.get('date')}) - {total_artists} artistas")

print(f"\n✅ {len(eventos_data)} eventos insertados\n")

print("=" * 60)
print("🎉 ¡SINCRONIZACIÓN COMPLETADA EXITOSAMENTE!")
print("=" * 60)
print(f"\n📊 RESUMEN:")
print(f"   • Artistas actualizados: {len(artistas_dict)}")
print(f"   • Eventos actualizados: {len(eventos_data)}")
print(f"\n✨ Firebase está sincronizado con los datos del frontend")
print(f"✨ Todos los artistas reales están en la base de datos")
print(f"✨ Los enlaces de Spotify están actualizados\n")
