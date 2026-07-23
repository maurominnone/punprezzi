import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

ZONES = {
    'IT-North': 'Zona Nord',
    'IT-Centre-North': 'Zona Centro-Nord',
    'IT-Centre-South': 'Zona Centro-Sud',
    'IT-South': 'Zona Sud',
    'IT-Calabria': 'Zona Calabria',
    'IT-Sicily': 'Zona Sicilia',
    'IT-Sardinia': 'Zona Sardegna',
}

OUT = Path('data/latest.json')
OUT.parent.mkdir(parents=True, exist_ok=True)

old_payload = None
if OUT.exists():
    try:
        old_payload = json.loads(OUT.read_text(encoding='utf-8'))
    except Exception:
        old_payload = None

now = datetime.now(timezone.utc)
start = (now - timedelta(days=1)).date().isoformat()
end = (now + timedelta(days=2)).date().isoformat()

payload = {
    'generatedAt': datetime.now().astimezone().isoformat(),
    'source': 'Energy-Charts',
    'stale': False,
    'lastError': None,
    'zones': {},
}

errors = []
success = 0

for zone, label in ZONES.items():
    params = urllib.parse.urlencode({'bzn': zone, 'start': start, 'end': end})
    url = f'https://api.energy-charts.info/price?{params}'
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            raw = resp.read().decode('utf-8')
        data = json.loads(raw)
        if not data.get('unix_seconds') or not data.get('price'):
            raise ValueError('Risposta vuota')
        payload['zones'][zone] = {'label': label, 'data': data, 'fetchedAt': datetime.now().astimezone().isoformat()}
        success += 1
    except Exception as exc:
        errors.append(f'{zone}: {exc}')
        if old_payload and old_payload.get('zones', {}).get(zone):
            payload['zones'][zone] = old_payload['zones'][zone]

if success == 0 and old_payload:
    old_payload['stale'] = True
    old_payload['generatedAt'] = datetime.now().astimezone().isoformat()
    old_payload['lastError'] = '; '.join(errors)[:500]
    OUT.write_text(json.dumps(old_payload, ensure_ascii=False, indent=2), encoding='utf-8')
elif success == 0:
    raise SystemExit('Nessun aggiornamento riuscito e nessun file precedente disponibile')
else:
    payload['stale'] = len(errors) > 0
    payload['lastError'] = '; '.join(errors)[:500] if errors else None
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
