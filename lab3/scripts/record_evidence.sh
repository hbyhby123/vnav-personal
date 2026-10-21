#!/usr/bin/env bash
# Record a ROS bag and an RViz desktop video with matching filenames.
set -eo pipefail
source /opt/ros/noetic/setup.bash
source "$HOME/vnav_ws/devel/setup.bash"
for program in ffmpeg xdpyinfo rosbag rosparam; do
  if ! command -v "$program" >/dev/null 2>&1; then
    echo "Missing command: $program. Install ffmpeg x11-utils or source ROS." >&2
    exit 1
  fi
done
if [ "${XDG_SESSION_TYPE:-x11}" = "wayland" ]; then
  echo "Use the Ubuntu on Xorg login session for this X11 screen recorder." >&2
  exit 1
fi
if [ -z "${DISPLAY:-}" ]; then
  echo "No desktop DISPLAY. Run this script inside the Ubuntu desktop terminal." >&2
  exit 1
fi
screen_size=$(xdpyinfo | awk '/dimensions:/{print $2}')
if [ -z "$screen_size" ]; then
  echo "Unable to read screen dimensions." >&2
  exit 1
fi
evidence_dir="$HOME/lab3_evidence"
mkdir -p "$evidence_dir"
run_tag=$(date +%Y%m%d_%H%M%S)
bag_path="$evidence_dir/circle_tracking_${run_tag}.bag"
video_path="$evidence_dir/V01_RViz_circle_${run_tag}.mp4"
param_path="$evidence_dir/parameters_${run_tag}.txt"
for key in kx kv kr komega; do
  value=$(rosparam get "/$key")
  printf '%s=%s\n' "$key" "$value" >> "$param_path"
done
bag_pid=""
cleanup() {
  if [ -n "$bag_pid" ] && kill -0 "$bag_pid" 2>/dev/null; then
    kill -INT "$bag_pid" 2>/dev/null || true
    wait "$bag_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT
trap 'exit 130' INT TERM
rosbag record --duration=45 -O "$bag_path" \
  /desired_state /current_state /rotor_speed_cmds /clock \
  > "$evidence_dir/record_${run_tag}.log" 2>&1 &
bag_pid=$!
echo "ROS bag recording started. Switch to RViz and maximize it within 5 seconds."
echo "Video records 40 seconds; ROS bag records 45 seconds of ROS time."
echo "Keep Unity running. Do not resize the Ubuntu desktop while recording."
sleep 5
if ! kill -0 "$bag_pid" 2>/dev/null; then
  cat "$evidence_dir/record_${run_tag}.log" >&2
  exit 1
fi
ffmpeg -hide_banner -loglevel warning -n \
  -f x11grab -framerate 15 -video_size "$screen_size" -i "$DISPLAY" \
  -t 40 -vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2' \
  -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p \
  "$video_path"
# ROS time may run slower than wall time. Finalize the bag after video ends.
cleanup
bag_pid=""
echo "Saved video: $video_path"
echo "Saved ROS bag: $bag_path"
echo "Saved gain values: $param_path"
