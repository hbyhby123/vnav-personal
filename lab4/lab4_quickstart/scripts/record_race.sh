#!/usr/bin/env bash
# Start this BEFORE publishing the race waypoints. Press Enter after finishing.
set -eo pipefail
source /opt/ros/noetic/setup.bash
source "$HOME/vnav_ws/devel/setup.bash"
for program in ffmpeg xdpyinfo rosbag rosparam rostopic; do
  command -v "$program" >/dev/null || { echo "Missing: $program"; exit 1; }
done
if [ -z "${DISPLAY:-}" ] || [ "${XDG_SESSION_TYPE:-x11}" = wayland ]; then
  echo 'Use an Ubuntu on Xorg desktop session for X11 screen recording.'; exit 1
fi
rostopic type /current_state
rostopic type /desired_state
run_dir="$HOME/lab4_evidence/runs/run_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$run_dir"
rosparam dump "$run_dir/parameters.yaml"
rostopic info /desired_state > "$run_dir/desired_state_publishers.txt"
cp -a "$HOME/vnav_ws/src/planner_pkg/src/simple_traj_planner.cpp" "$run_dir/"
cp -a "$HOME/vnav_ws/src/trajectory_generation_pkg/src/trajectory_generation_node.cpp" "$run_dir/"
cp -a "$HOME/vnav_ws/src/trajectory_generation_pkg/launch/traj_following.launch" "$run_dir/"
date --iso-8601=seconds > "$run_dir/record_start.txt"
screen_size="$(xdpyinfo | awk '/dimensions:/{print $2}')"
test -n "$screen_size" || { echo 'Could not read desktop dimensions'; exit 1; }
bag_pid=''
video_pid=''
finish() {
  trap - EXIT INT TERM
  if [ -n "$video_pid" ]; then kill -INT "$video_pid" 2>/dev/null || true; wait "$video_pid" || true; fi
  if [ -n "$bag_pid" ]; then kill -INT "$bag_pid" 2>/dev/null || true; wait "$bag_pid" || true; fi
  if [ -f "$run_dir/race.bag" ]; then rosbag info "$run_dir/race.bag" > "$run_dir/bag_info.txt"; fi
  echo "Saved: $run_dir"
  echo 'Check video playback and bag topics before choosing this as a valid run.'
}
trap finish EXIT INT TERM
rosbag record -O "$run_dir/race.bag" /current_state /desired_state /desired_traj_vertices /rotor_speed_cmds /clock > "$run_dir/rosbag.log" 2>&1 &
bag_pid=$!
sleep 2
kill -0 "$bag_pid" 2>/dev/null || { echo 'Bag recorder failed; inspect rosbag.log'; exit 1; }
echo 'Recording begins in 5 seconds. Arrange Unity/RViz, then start the waypoint publisher in another terminal.'
sleep 5
ffmpeg -nostdin -y -f x11grab -framerate 20 -video_size "$screen_size" -i "${DISPLAY}+0,0" -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p "$run_dir/race.mp4" > "$run_dir/ffmpeg.log" 2>&1 &
video_pid=$!
sleep 2
kill -0 "$video_pid" 2>/dev/null || { echo 'Video recorder failed; inspect ffmpeg.log'; exit 1; }
echo 'Video and bag recording. NOW launch planner_pkg traj_gen.launch in another terminal.'
read -r -p 'After passing all gates, wait 3 seconds, return here and press Enter to save: ' || true
