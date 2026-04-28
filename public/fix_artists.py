import json

with open('eventos-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

artist_map = {
  'The Sonic Masters': { 'name': 'Daft Punk', 'url': 'https://open.spotify.com/artist/4tZwfgrHOc3mvqYlEYSvVi' },
  'Luna Sky': { 'name': 'Billie Eilish', 'url': 'https://open.spotify.com/artist/6qqNVTkY8uBg9cP3Jd7DAH' },
  'Rhythm & Beats': { 'name': 'Kendrick Lamar', 'url': 'https://open.spotify.com/artist/2YZyLoL8N0Wb9xBt1NhZWg' },
  'Urban Beats': { 'name': 'Bad Bunny', 'url': 'https://open.spotify.com/artist/4q3ewBCX7sLwd24euuV69X' },
  'Electric Horizon': { 'name': 'Arctic Monkeys', 'url': 'https://open.spotify.com/artist/7Ln80lUS6He07XvHI8qqHH' },
  'Deep Groove Collective': { 'name': 'Jamiroquai', 'url': 'https://open.spotify.com/artist/6P7H3ai06vU1QET6zQX4Ms' },
  'Cyber Pulse': { 'name': 'The Prodigy', 'url': 'https://open.spotify.com/artist/4k1ELeJKT1ISyDV8Jp5AQx' },
  'Jazz Collective': { 'name': 'Thundercat', 'url': 'https://open.spotify.com/artist/4cpNBphiDqkOWyfoOPdbEi' },
  'Classical Chaos': { 'name': 'Hans Zimmer', 'url': 'https://open.spotify.com/artist/0YC192cP3KpqHKWUOUpt9T' },
  'Melodic Echoes': { 'name': 'Tame Impala', 'url': 'https://open.spotify.com/artist/5INjqkS1o8h1imAzPqGZKp' },
  'Neon Pulse': { 'name': 'The Weeknd', 'url': 'https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpzMBGW3o' },
  'Solar Waves': { 'name': 'Calvin Harris', 'url': 'https://open.spotify.com/artist/7CajNmpbOovFoOoasH2HaY' },
  'Sonic Velocity': { 'name': 'Tiësto', 'url': 'https://open.spotify.com/artist/2o5jDhtHVPhrJdv3cEQ99Z' },
  'Neon Dream': { 'name': 'Dua Lipa', 'url': 'https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we' },
  'Sonic Waves': { 'name': 'Skrillex', 'url': 'https://open.spotify.com/artist/5he5w2lnU9x7JFhnwcekXX' },
  'Urban Pulse': { 'name': 'Travis Scott', 'url': 'https://open.spotify.com/artist/0Y5tJX1MQlPlqiwlOH1tJY' }
}

for evento in data.get('principales', []):
    for escenario, artistas in evento.get('artists', {}).items():
        for artista in artistas:
            if artista['name'] in artist_map:
                info = artist_map[artista['name']]
                artista['name'] = info['name']
                artista['spotify_url'] = info['url']

with open('eventos-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open('eventos-data.js', 'w', encoding='utf-8') as f:
    f.write('window.EVENTOS_DATA = ' + json.dumps(data, indent=2, ensure_ascii=False) + ';')

print('Reemplazo completado correctamente con Python')