#!/usr/bin/env python3
"""
Script para verificar si los IDs de Spotify son válidos
"""
import requests
import json
from pathlib import Path

# Cargar los datos del JSON
json_path = Path(__file__).parent / "public" / "eventos-data.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraer todos los IDs de Spotify
spotify_urls = set()
eventos = data.get("principales", [])

for evento in eventos:
    artists = evento.get("artists", {})
    if isinstance(artists, dict):
        for escenario, artist_list in artists.items():
            for artist in artist_list:
                url = artist.get("spotify_url", "")
                if url:
                    spotify_urls.add((artist.get("name"), url))

print("🎵 Verificando URLs de Spotify...\n")
print("=" * 70)

valid_count = 0
invalid_count = 0

for artist_name, url in sorted(spotify_urls):
    # Extraer el ID
    if "/artist/" in url:
        artist_id = url.split("/artist/")[-1]
    else:
        print(f"❌ {artist_name}: URL mal formada - {url}")
        invalid_count += 1
        continue
    
    print(f"\n🎤 {artist_name}")
    print(f"   ID: {artist_id}")
    print(f"   URL: {url}")
    
    # Intentar acceder a la URL (solo verificar si es accesible)
    try:
        # Spotify no permite scraping, pero podemos intentar una búsqueda en la API
        # En su lugar, simplemente validamos que sea una URL válida
        if len(artist_id) == 22:
            print(f"   ✓ ID válido (22 caracteres)")
            valid_count += 1
        else:
            print(f"   ❌ ID inválido (tiene {len(artist_id)} caracteres, necesita 22)")
            invalid_count += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        invalid_count += 1

print("\n" + "=" * 70)
print(f"\n📊 RESUMEN:")
print(f"   ✓ URLs válidas: {valid_count}")
print(f"   ❌ URLs inválidas: {invalid_count}")
