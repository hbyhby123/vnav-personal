"""Prepare Lab4 edits against the specified official starter version."""
from pathlib import Path
import urllib.request
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1] / 'patches'
base = 'https://raw.githubusercontent.com/MIT-SPARK/VNAV-labs/VNAV2021/lab4/'
paths = ['planner_pkg/src/simple_traj_planner.cpp',
         'trajectory_generation_pkg/src/trajectory_generation_node.cpp',
         'planner_pkg/launch/static_point_test.launch',
         'planner_pkg/launch/traj_gen.launch',
         'trajectory_generation_pkg/launch/traj_following.launch']

part0 = '''
  const auto& pose = traj_msg.poses.front();
  trajectory_msgs::MultiDOFJointTrajectoryPoint point;
  geometry_msgs::Transform transform;
  transform.translation.x = pose.position.x;
  transform.translation.y = pose.position.y;
  transform.translation.z = pose.position.z;
  transform.rotation = pose.orientation;
  point.transforms.push_back(transform);
  point.velocities.emplace_back();
  point.accelerations.emplace_back();
  point.time_from_start = ros::Duration(0.0);
  desired_state_pub.publish(point);
  tf::Transform desired;
  desired.setOrigin(tf::Vector3(pose.position.x, pose.position.y, pose.position.z));
  tf::Quaternion q;
  tf::quaternionMsgToTF(pose.orientation, q);
  q.normalize();
  desired.setRotation(q);
  br->sendTransform(tf::StampedTransform(desired, ros::Time::now(), "world", "desired_pose"));
'''
part11 = '''
    x << cur_state.pose.pose.position.x, cur_state.pose.pose.position.y,
         cur_state.pose.pose.position.z;
    current_yaw = tf::getYaw(cur_state.pose.pose.orientation);
    have_current = x.allFinite() && std::isfinite(current_yaw);
'''
part12_position = '''
      const auto& pose = poseArray.poses[i];
      Eigen::Vector3d position(pose.position.x, pose.position.y, pose.position.z);
      mav_trajectory_generation::Vertex vertex(D);
      if (i + 1 == poseArray.poses.size())
        vertex.makeStartOrEnd(position, SNAP);
      else
        vertex.addConstraint(POSITION, position);
      vertices.push_back(vertex);
'''
part12_yaw = '''
      double yaw = tf::getYaw(pose.orientation);
      yaw = last_yaw + std::atan2(std::sin(yaw - last_yaw), std::cos(yaw - last_yaw));
      mav_trajectory_generation::Vertex yaw_vertex(1);
      Eigen::VectorXd yaw_value(1);
      yaw_value << yaw;
      if (i + 1 == poseArray.poses.size())
        yaw_vertex.makeStartOrEnd(yaw_value, SNAP);
      else
        yaw_vertex.addConstraint(ORIENTATION, yaw);
      yaw_vertices.push_back(yaw_vertex);
      last_yaw = yaw;
'''
part13 = '''
    geometry_msgs::Transform transform;
    transform.translation.x = des_position.x();
    transform.translation.y = des_position.y();
    transform.translation.z = des_position.z();
    transform.rotation = tf::createQuaternionMsgFromYaw(des_orientation(0));
    geometry_msgs::Twist velocity, acceleration;
    velocity.linear.x = des_velocity.x();
    velocity.linear.y = des_velocity.y();
    velocity.linear.z = des_velocity.z();
    acceleration.linear.x = des_accel.x();
    acceleration.linear.y = des_accel.y();
    acceleration.linear.z = des_accel.z();
    next_point.transforms.push_back(transform);
    next_point.velocities.push_back(velocity);
    next_point.accelerations.push_back(acceleration);
    desiredStatePub.publish(next_point);
'''

for path in paths:
    text = urllib.request.urlopen(base + path, timeout=45).read().decode().replace('\r\n', '\n')
    if path.endswith('simple_traj_planner.cpp'):
        text, count = re.subn(r'^[ \t]*//\s*\*{4} FILL IN HERE \*{3}.*$', lambda m: part0,
                              text, flags=re.M)
        assert count == 1, ('Part0 template changed', count)
    elif path.endswith('trajectory_generation_node.cpp'):
        blocks = iter([part11, part12_position, part12_yaw, part13])
        text, count = re.subn(r'^[ \t]*//\s*\*{4} FILL IN HERE \*{3}.*$',
                              lambda m: next(blocks), text, flags=re.M)
        assert count == 4, ('Part1 template changed', count)
        text = '#include <algorithm>\n#include <cmath>\n' + text
        text = text.replace('Eigen::Vector3d x;', 'bool have_current = false;\n  double current_yaw = 0;\n  double time_scale = 2.0;\n  Eigen::Vector3d x;')
        text = text.replace('if (poseArray.poses.size() < 1)',
                            'if (!have_current) { ROS_WARN_THROTTLE(1.0, "Waiting for current state"); return; }\n    if (poseArray.poses.size() < 1)')
        text = text.replace('start_yaw.addConstraint(ORIENTATION, 0);',
                            'Eigen::VectorXd initial_yaw(1); initial_yaw << current_yaw;\n    start_yaw.makeStartOrEnd(initial_yaw, SNAP);')
        text = text.replace('double last_yaw = 0;', 'double last_yaw = current_yaw;')
        text = text.replace('segment_times = estimateSegmentTimes(vertices, v_max, a_max);',
                            'segment_times = estimateSegmentTimes(vertices, v_max, a_max);\n    for (auto& duration : segment_times) duration *= time_scale;')
        text, count = re.subn(r'next_point.time_from_start = ros::Duration\(0\.0\);[^\n]*\n\s*double sampling_time = 0;[^\n]*',
                             'double sampling_time = std::max(0.0, (ros::Time::now() - trajectoryStartTime).toSec());', text)
        assert count == 1, 'Sampling-time template changed'
        text = text.replace('sampling_time = trajectory.getMaxTime();',
                            'sampling_time = trajectory.getMaxTime();\n    next_point.time_from_start = ros::Duration(sampling_time);')
        text = text.replace('ROS_INFO("Traversed %f percent of the trajectory.",',
                            'ROS_INFO_THROTTLE(1.0, "Traversed %f percent of the trajectory.",')
        text = text.replace('vertices.size());', 'static_cast<int>(vertices.size()));')
        text = text.replace('explicit WaypointFollower(ros::NodeHandle& nh) {',
                            'explicit WaypointFollower(ros::NodeHandle& nh) {\n    ros::NodeHandle private_nh("~");\n    private_nh.param("time_scale", time_scale, 2.0);\n    if (!std::isfinite(time_scale) || time_scale < 1.0) time_scale = 1.0;')
        text = text.replace('ros::Rate(5), &WaypointFollower::publishDesiredState',
                            'ros::Rate(50), &WaypointFollower::publishDesiredState')
    else:
        tree = ET.fromstring(text)
        if not path.endswith('traj_gen.launch'):
            for name, value in [('kx', '2.0'), ('kv', '3.0'), ('kr', '3.0'), ('komega', '1.0')]:
                ET.SubElement(tree, 'arg', name=name, default=value)
                ET.SubElement(tree, 'param', name=name, value='$(arg '+name+')')
        if path.endswith('traj_following.launch'):
            ET.SubElement(tree, 'arg', name='time_scale', default='2.0')
            node = next(n for n in tree.findall('node') if n.get('name') == 'trajectory_generation_node')
            ET.SubElement(node, 'param', name='time_scale', value='$(arg time_scale)')
        text = ET.tostring(tree, encoding='unicode') + '\n'
    assert 'FILL IN HERE' not in text, path
    assert '<--- Correct this' not in text, path
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8', newline='\n')
print('Prepared five Lab4 files. Runtime compilation and flight must be checked on Ubuntu.')
