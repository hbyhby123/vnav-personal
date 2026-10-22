#!/usr/bin/env bash
# Cache the original NLopt archive, verify it, and resume the build.
set -Ee -o pipefail
source /opt/ros/noetic/setup.bash
mkdir -p "$HOME/lab4_evidence/downloads" "$HOME/lab4_evidence/logs"
log="$HOME/lab4_evidence/logs/nlopt_$(date +%Y%m%d_%H%M%S).txt"
exec > >(tee -a "$log") 2>&1
trap 'echo "Repair stopped. Send this log: $log"' ERR
wget --tries=3 --timeout=30 \
  -O "$HOME/lab4_evidence/downloads/nlopt-2.4.2.tar.gz" \
  https://raw.githubusercontent.com/ethz-asl/thirdparty_library_binaries/master/nlopt-2.4.2.tar.gz
echo "8099633de9d71cbc06cd435da993eb424bbcdbded8f803cdaa9fb8c6e09c8e89  $HOME/lab4_evidence/downloads/nlopt-2.4.2.tar.gz" | sha256sum -c -
python3 - <<'PY'
from pathlib import Path
import re
p = Path.home() / 'vnav_ws/src/dependencies/nlopt/CMakeLists.txt'
archive = Path.home() / 'lab4_evidence/downloads/nlopt-2.4.2.tar.gz'
text = p.read_text()
if 'set(VERSION 2.4.2)' not in text:
    raise SystemExit('Unexpected NLopt version; send CMakeLists.txt.')
backup = p.with_name('CMakeLists.txt.before_download_fix')
if not backup.exists():
    backup.write_bytes(p.read_bytes())
replacement = ('  DOWNLOAD_COMMAND ${CMAKE_COMMAND} -E copy '
               f'"{archive}" "<DOWNLOAD_DIR>/nlopt-${{VERSION}}.tar.gz"')
text, count = re.subn(r'(?m)^[ \t]*DOWNLOAD_COMMAND[^\n]*$',
                     lambda match: replacement, text)
if count != 1:
    raise SystemExit('Unexpected download configuration; original left intact.')
p.write_text(text)
print('NLopt now uses the verified local archive.')
PY
cd "$HOME/vnav_ws"
catkin build nlopt --force-cmake -j2 -p1
catkin build -j2 -p1
source devel/setup.bash
echo "Build completed. Log: $log"
