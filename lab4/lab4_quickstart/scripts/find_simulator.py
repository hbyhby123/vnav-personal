"""Resolve the Lab4 executable from the exact gate-map CSV required by the starter."""
from pathlib import Path
import shlex

base = Path.home() / 'vnav-builds'
maps = list(base.rglob('vnav-2020-lab4_static_tfs.csv'))
choices = []
for gate_map in maps:
    data = gate_map.parent.parent
    stem = data.name[:-5] if data.name.endswith('_Data') else data.name
    exact = data.parent / (stem + '.x86_64')
    candidates = [exact] if exact.is_file() else list(data.parent.glob('*.x86_64'))
    if len(candidates) == 1:
        choices.append((candidates[0], data))
if len(choices) != 1:
    print('Expected one Lab4 simulator with the required gate-map CSV; found:', len(choices))
    for entry in choices:
        print(*entry)
    raise SystemExit('Send this output and the simulator directory listing before continuing.')
exe, data = choices[0]
exe.chmod(exe.stat().st_mode | 0o111)
out = Path.home() / 'lab4_evidence' / 'sim.env'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('SIM_EXEC=' + shlex.quote(str(exe)) + '\nSIM_DATA=' + shlex.quote(str(data)) + '\n')
print(out.read_text())
print('Saved:', out)
