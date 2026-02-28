#!/usr/bin/env python3
"""Copy today's history.json into data/daily/YYYY-MM-DD.json and update manifest."""
import json, shutil, os
from datetime import datetime, timezone

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(base, 'data', 'history.json')
daily_dir = os.path.join(base, 'data', 'daily')
manifest_path = os.path.join(daily_dir, 'manifest.json')

os.makedirs(daily_dir, exist_ok=True)

with open(src) as f:
    data = json.load(f)

date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
dest = os.path.join(daily_dir, f'{date_str}.json')
shutil.copy2(src, dest)
print(f'Saved snapshot: {date_str}.json')

# Update manifest
try:
    with open(manifest_path) as f:
        raw = json.load(f)
        if isinstance(raw, dict):
            manifest = raw
        else:
            manifest = {'dates': []}
except:
    manifest = {'dates': []}

dates = set(manifest.get('dates', []))
dates.add(date_str)
manifest['dates'] = sorted(dates)
manifest['last_updated'] = datetime.now(timezone.utc).isoformat()

with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'Manifest updated: {len(manifest["dates"])} days')
