#!/usr/bin/env bash
# Preserve source files, add the missing source dependency, rebuild moved packages.
set -Ee -o pipefail
mkdir -p "$HOME/lab4_evidence/logs"
stamp="$(date +%Y%m%d_%H%M%S)"
log="$HOME/lab4_evidence/logs/repair_$stamp.txt"
exec > >(tee -a "$log") 2>&1
trap 'echo "Repair stopped. Send this log: $log"' ERR
source /opt/ros/noetic/setup.bash
test -d "$HOME/vnav_ws/src/dependencies/catkin_simple"
sudo apt-get install -y autoconf automake libtool patch pkg-config libgflags-dev
if ! grep -R -q '<name>gflags_catkin</name>' "$HOME/vnav_ws/src" --include=package.xml; then
  git clone --depth 1 https://github.com/ethz-asl/gflags_catkin.git \
    "$HOME/vnav_ws/src/dependencies/gflags_catkin"
fi
rosdep install --from-paths "$HOME/vnav_ws/src" --ignore-src --rosdistro noetic -r -y
backup="$HOME/lab4_evidence/backups/rebuild_$stamp"
mkdir -p "$backup"
for space in build devel; do
  if [ -d "$HOME/vnav_ws/$space" ]; then
    mv "$HOME/vnav_ws/$space" "$backup/$space"
  fi
done
cd "$HOME/vnav_ws"
catkin config --extend /opt/ros/noetic
catkin build -j2 -p1
source devel/setup.bash
rospack find controller_pkg
rospack find planner_pkg
rospack find trajectory_generation
echo "Repair build succeeded. Log: $log"
echo 'Simulator setup was not reached in the failed run; continue with manual section A4.'
