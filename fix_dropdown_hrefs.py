#!/usr/bin/env python3
"""
Script para arreglar todos los href de dropdown de Eventos en los archivos HTML
"""
import re
from pathlib import Path

# Mapeo de ciudades a IDs
cities_map = {
    'madrid': 'madrid',
    'barcelona': 'barcelona',
    'valencia': 'valencia',
    'bilbao': 'bilbao',
    'sevilla': 'sevilla',
    'málaga': 'malaga',
    'malaga': 'malaga'
}

# Buscar todos los archivos HTML
public_dir = Path(__file__).parent / "public"
html_files = list(public_dir.glob("*.html"))

print(f"🔍 Encontrados {len(html_files)} archivos HTML\n")

updated_count = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Reemplazar todos los href="eventos.html#ciudad" por href="evento-detail.html?id=ciudad"
    for city_lower, city_id in cities_map.items():
        old_href = f'href="eventos.html#{city_lower}"'
        new_href = f'href="evento-detail.html?id={city_id}"'
        
        if old_href in content:
            content = content.replace(old_href, new_href)
            print(f"✓ {html_file.name}: {city_lower} -> evento-detail.html?id={city_id}")
    
    # Si hubo cambios, guardar el archivo
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1
        print(f"  📝 Guardado: {html_file.name}\n")

print(f"\n✅ {updated_count} archivos actualizados")
