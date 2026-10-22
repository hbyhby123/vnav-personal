#!/usr/bin/env bash
# ROS Noetic is already installed. Final archived packages must be copied first.
set -Ee -o pipefail
source /opt/ros/noetic/setup.bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sudo apt-get update
sudo apt-get install -y git wget unzip build-essential cmake pkg-config \
  python3-pip python3-catkin-tools python3-rosdep python3-numpy python3-scipy \
  python3-matplotlib python3-defusedxml python3-pil \
  libeigen3-dev libboost-all-dev libgoogle-glog-dev libgflags-dev \
  libyaml-cpp-dev libnlopt-dev autoconf automake libtool patch ffmpeg x11-utils \
  ros-noetic-ackermann-msgs ros-noetic-cmake-modules ros-noetic-eigen-conversions \
  ros-noetic-tf2-eigen ros-noetic-tf2-geometry-msgs ros-noetic-rviz
mkdir -p "$HOME/lab4_evidence/install_sources" "$HOME/vnav_ws/src"
source_dir="$HOME/lab4_evidence/install_sources/VNAV2021"
if [ ! -d "$source_dir/lab4" ]; then
  git clone --depth 1 --branch VNAV2021 https://github.com/MIT-SPARK/VNAV-labs.git "$source_dir"
fi
if [ ! -d "$HOME/vnav_ws/src/controller_pkg" ]; then
  echo 'Copy the three archived final packages first; see the fresh-setup instructions.'; exit 1
fi
cp -an "$source_dir/lab4/dependencies" "$HOME/vnav_ws/src/"
if [ ! -d "$HOME/vnav_ws/src/tesse-ros-bridge" ]; then
  cp -a "$source_dir/lab3/tesse-ros-bridge" "$HOME/vnav_ws/src/"
  python3 -m pip install --user -r "$HOME/vnav_ws/src/tesse-ros-bridge/tesse-interface/requirements.txt"
  python3 -m pip install --user "$HOME/vnav_ws/src/tesse-ros-bridge/tesse-interface"
fi
backup="$HOME/lab4_evidence/backups/dependencies_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup"
moved=0
for dependency in "$HOME/vnav_ws/src/dependencies/"*/; do
  [ -d "$dependency" ] || continue
  name="$(basename "$dependency")"
  if [ -d "$HOME/vnav_ws/src/$name" ]; then
    mv "$HOME/vnav_ws/src/$name" "$backup/${name}_standalone"; moved=1
  fi
done
if ! grep -R -q '<name>gflags_catkin</name>' "$HOME/vnav_ws/src" --include=package.xml; then
  git clone --depth 1 https://github.com/ethz-asl/gflags_catkin.git "$HOME/vnav_ws/src/dependencies/gflags_catkin"
fi
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then sudo rosdep init; fi
rosdep update --include-eol-distros
rosdep install --from-paths "$HOME/vnav_ws/src" --ignore-src --rosdistro noetic -r -y
if [ "$moved" = 1 ]; then
  for space in build devel; do
    if [ -d "$HOME/vnav_ws/$space" ]; then mv "$HOME/vnav_ws/$space" "$backup/$space"; fi
  done
fi
cd "$HOME/vnav_ws"
catkin config --extend /opt/ros/noetic
bash "$script_dir/repair_nlopt.sh"
