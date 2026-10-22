#!/usr/bin/env bash
# Install the archived Lab4 packages in a configured workspace.
set -Ee -o pipefail
source /opt/ros/noetic/setup.bash
stamp="$(date +%Y%m%d_%H%M%S)"
backup="$HOME/lab4_evidence/backups/install_$stamp"
cache="$HOME/lab4_evidence/install_sources/vnav-personal"
mkdir -p "$backup" "$HOME/vnav_ws/src" "$(dirname "$cache")"
if [ ! -d "$cache/.git" ]; then
  git clone --depth 1 --filter=blob:none --sparse https://github.com/hbyhby123/vnav-personal.git "$cache"
  git -C "$cache" sparse-checkout set lab4/code lab4/review/scripts
else
  if [ -n "$(git -C "$cache" status --porcelain)" ]; then
    echo "Install cache has local edits. Preserve them before updating: $cache"; exit 1
  fi
  git -C "$cache" pull --ff-only
fi
for name in controller_pkg planner_pkg trajectory_generation_pkg; do
  if [ -d "$HOME/vnav_ws/src/$name" ]; then cp -a "$HOME/vnav_ws/src/$name" "$backup/"; fi
  cp -a "$cache/lab4/code/$name" "$HOME/vnav_ws/src/"
done
cd "$HOME/vnav_ws"
catkin build -j2 -p1
echo "Installed archived packages. Backup: $backup"
echo 'Use the Lab4 launch files, not the old Lab3 traj_tracking.launch.'
