#!/usr/bin/env bash
# Install Lab4 only. Preserve the working Lab3 controller and bridge.
set -eo pipefail
source /opt/ros/noetic/setup.bash
bundle_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
stamp="$(date +%Y%m%d_%H%M%S)"
backup="$HOME/lab4_evidence/backups/$stamp"
mkdir -p "$backup" "$HOME/vnav_ws/src" "$HOME/lab4_evidence/logs"
test -f "$HOME/vnav_ws/src/controller_pkg/src/controller_node.cpp" || {
  echo 'Missing completed Lab3 controller. Restore Lab3 before installing Lab4.'; exit 1;
}
if [ ! -d "$HOME/labs/lab4" ]; then
  if [ -e "$HOME/labs" ]; then
    echo 'Existing ~/labs has no lab4. Send its directory listing before continuing.'; exit 1
  fi
  git clone --branch VNAV2021 --depth 1 https://github.com/MIT-SPARK/VNAV-labs.git "$HOME/labs"
fi
for name in planner_pkg trajectory_generation_pkg dependencies; do
  if [ -e "$HOME/vnav_ws/src/$name" ]; then
    cp -a "$HOME/vnav_ws/src/$name" "$backup/"
  fi
done
# Add missing original files; patched files are deliberately installed below.
cp -an "$HOME/labs/lab4/." "$HOME/vnav_ws/src/"
for dependency in "$HOME/vnav_ws/src/dependencies/"*/; do
  [ -d "$dependency" ] || continue
  name="$(basename "$dependency")"
  if [ -d "$HOME/vnav_ws/src/$name" ]; then
    mv "$HOME/vnav_ws/src/$name" "$backup/${name}_standalone"
  fi
done
if ! grep -R -q '<name>gflags_catkin</name>' "$HOME/vnav_ws/src" --include=package.xml; then
  git clone --depth 1 https://github.com/ethz-asl/gflags_catkin.git \
    "$HOME/vnav_ws/src/dependencies/gflags_catkin"
fi
# Install only program patches; keep repository documentation out of the ROS tree.
for relative_path in \
  planner_pkg/src/simple_traj_planner.cpp \
  planner_pkg/launch/static_point_test.launch \
  planner_pkg/launch/traj_gen.launch \
  trajectory_generation_pkg/src/trajectory_generation_node.cpp \
  trajectory_generation_pkg/launch/traj_following.launch; do
  mkdir -p "$(dirname "$HOME/vnav_ws/src/$relative_path")"
  cp -a "$bundle_dir/patches/$relative_path" "$HOME/vnav_ws/src/$relative_path"
done
cd "$HOME/vnav_ws"
for space in build devel; do
  if [ -d "$HOME/vnav_ws/$space" ]; then
    mv "$HOME/vnav_ws/$space" "$backup/$space"
  fi
done
catkin config --extend /opt/ros/noetic
catkin build 2>&1 | tee "$HOME/lab4_evidence/logs/build_$stamp.txt"
echo "Lab4 installed. Lab3 controller was preserved. Backup: $backup"
echo 'Next: source ~/vnav_ws/devel/setup.bash'
