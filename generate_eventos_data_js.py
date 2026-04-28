#!/usr/bin/env python3
"""
Script para generar eventos-data.js desde eventos-data.json
"""
import json
from pathlib import Path

# Leer el JSON correcto
json_path = Path(__file__).parent / "public" / "eventos-data.json"

with open(json_path, 'r', encoding='utf-8') as f:
    eventos_data = json.load(f)

# Generar el contenido de eventos-data.js
js_content = f"""window.EVENTOS_DATA = {json.dumps(eventos_data, ensure_ascii=False, indent=2)};
"""

# Escribir el archivo
js_path = Path(__file__).parent / "public" / "eventos-data.js"

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ Archivo generado: {js_path}")
print(f"📊 {len(eventos_data.get('principales', []))} eventos incluidos")

# Verificar que se escribió correctamente
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()
    if 'window.EVENTOS_DATA' in content and 'The Weeknd' in content:
        print("✓ Contenido verificado - incluye datos correctos")
    else:
        print("❌ Error en la verificación")
