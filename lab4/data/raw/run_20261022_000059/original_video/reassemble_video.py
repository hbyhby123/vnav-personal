"""Join GitHub-sized parts, verify SHA256, and recover the exact original video."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
manifest = json.loads((base / 'manifest.json').read_text())
output = base.parent / 'race_original.mp4'
for part in manifest['parts']:
    p = base / part['file']
    if p.stat().st_size != part['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != part['sha256']:
        raise SystemExit('Missing or damaged part: ' + str(p))
if output.exists():
    if hashlib.sha256(output.read_bytes()).hexdigest() == manifest['original_sha256']:
        print('Verified existing original:', output)
        raise SystemExit(0)
    raise SystemExit('Output already exists with different content; choose another path first.')
temporary = output.with_suffix('.mp4.joining')
digest = hashlib.sha256()
with temporary.open('wb') as dest:
    for part in manifest['parts']:
        with (base / part['file']).open('rb') as src:
            while block := src.read(1024 * 1024):
                dest.write(block)
                digest.update(block)
if digest.hexdigest() != manifest['original_sha256']:
    raise SystemExit('Combined SHA256 differs; temporary file retained for inspection.')
temporary.rename(output)
print('Original recovered and SHA256 verified:', output)
