#!/usr/bin/env bash
# Download the three changed files; preserve a timestamped local backup.
set -eo pipefail
package_dir="$HOME/vnav_ws/src/controller_pkg"
evidence_dir="$HOME/lab3_evidence"
if [ ! -f "$package_dir/package.xml" ]; then
  echo "ERROR: controller_pkg is missing from $package_dir" >&2
  exit 1
fi
mkdir -p "$evidence_dir"
stage_dir=$(mktemp -d "$evidence_dir/controller_download.XXXXXX")
base_url="https://raw.githubusercontent.com/hbyhby123/vnav-personal/master/lab3/controller_pkg"
for relative_path in src/controller_node.cpp src/traj_publisher.cpp launch/traj_tracking.launch; do
  mkdir -p "$stage_dir/$(dirname "$relative_path")"
  wget --timeout=30 --tries=3 -O "$stage_dir/$relative_path" "$base_url/$relative_path"
done
# All downloads must finish before replacing any workspace file.
backup_dir=$(mktemp -d "$evidence_dir/controller_backup_$(date +%Y%m%d_%H%M%S).XXXXXX")
cp -a "$package_dir" "$backup_dir/controller_pkg"
printf 'Original controller package backed up to: %s\n' "$backup_dir/controller_pkg"
for relative_path in src/controller_node.cpp src/traj_publisher.cpp launch/traj_tracking.launch; do
  cp "$stage_dir/$relative_path" "$package_dir/$relative_path"
done
# A new installation always begins with hover, even when the archived package uses circle mode.
sed -i 's/^#define STATIC_POSE .*/#define STATIC_POSE 1/' "$package_dir/src/traj_publisher.cpp"
source /opt/ros/noetic/setup.bash
cd "$HOME/vnav_ws"
catkin build 2>&1 | tee "$evidence_dir/build_controller.log"
printf '\nBuild finished. Run: source ~/vnav_ws/devel/setup.bash\n'
printf 'Default mode is HOVER: target (0,0,2) m. Restart the controller to use new code.\n'
