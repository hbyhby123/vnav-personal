/*
 * Lab3 四旋翼控制器｜先看这里
 *
 * 本文件是已经补全的控制器，不是待填写模板。
 * 实验要求补全的11处代码均以“【实验要求补充 NN】”标出，可直接搜索。
 * 主线：读取目标和实际状态 → 计算误差 → 求推力与力矩 → 发布旋翼转速。
 *
 * 01-02：建立ROS通信；03-04：读取目标；05：读取实际状态。
 * 06-09：计算误差、期望姿态、推力和力矩；10-11：分配并发布旋翼转速。
 * 各处所在函数和具体作用见上层“00_先看这里_实验补全代码说明.md”。
 *
 * 配套实现：构造函数中的旋翼分配矩阵、初始状态和最终参数。
 * 原模板自带：Vee、signed_sqrt辅助函数及main入口，不列入11处补全。
 * 原始待补全文件位于 ../../original/controller_node_VNAV2021_待补全.cpp。
 *
 * 当前参数：kx=2、kv=3、kr=3、komega=1。
 * 当前实现未加入阻力补偿，也未加入目标角速度前馈。
 * 本次整理只改注释和格式，不改控制算法、参数或接口。
 */
#include <ros/ros.h>

#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/utils.h>
#include <mav_msgs/Actuators.h>
#include <nav_msgs/Odometry.h>
#include <trajectory_msgs/MultiDOFJointTrajectoryPoint.h>
#include <cmath>

#define PI M_PI

#include <eigen3/Eigen/Dense>

#include <tf2_eigen/tf2_eigen.h>

class controllerNode {
  ros::NodeHandle nh;

  // 【实验要求补充 01｜PART 1：通信成员声明】
  // 建立两个订阅器、一个发布器和控制定时器；状态标志用于启动检查。
  ros::Subscriber desired_sub, current_sub;
  ros::Publisher rotor_pub;
  ros::Timer control_timer;
  bool have_desired = false;
  bool have_current = false;

  double kx, kv, kr, komega;

  double m;
  double g;
  double d;
  double cf, cd;
  Eigen::Matrix3d J;
  Eigen::Vector3d e3;
  Eigen::MatrixXd F2W;

  Eigen::Vector3d x;
  Eigen::Vector3d v;
  Eigen::Matrix3d R;
  Eigen::Vector3d omega;

  Eigen::Vector3d xd;
  Eigen::Vector3d vd;
  Eigen::Vector3d ad;
  double yawd;

  double hz;

  // 【原模板辅助函数】把反对称矩阵还原为三维向量，供姿态误差计算使用。
  static Eigen::Vector3d Vee(const Eigen::Matrix3d &in) {
    Eigen::Vector3d out;
    out << in(2, 1), in(0, 2), in(1, 0);
    return out;
  }

  // 【原模板辅助函数】开平方时保留符号；仿真器允许负角速度。
  static double signed_sqrt(double val) { return val > 0 ? sqrt(val) : -sqrt(-val); }

public:
  controllerNode() : e3(0, 0, 1), F2W(4, 4), hz(1000.0) {

    // 【实验要求补充 02｜PART 2：通信初始化】
    // 把目标和实际状态消息接到回调；建立四旋翼转速发布器，注册定时控制函数。
    desired_sub = nh.subscribe("desired_state", 1, &controllerNode::onDesiredState, this);
    current_sub = nh.subscribe("current_state", 1, &controllerNode::onCurrentState, this);
    rotor_pub = nh.advertise<mav_msgs::Actuators>("rotor_speed_cmds", 1);
    control_timer = nh.createTimer(ros::Duration(1.0 / hz), &controllerNode::controlLoop, this);

    // 【调参设置】先从ROS参数读取，未设置时使用已验证的默认值。
    nh.param("kx", kx, 2.0);
    nh.param("kv", kv, 3.0);
    nh.param("kr", kr, 3.0);
    nh.param("komega", komega, 1.0);
    ROS_INFO("Gain values:\nkx: %f \nkv: %f \nkr: %f \nkomega: %f\n", kx, kv, kr, komega);

    // 【沿用源码常量】这些值未在本次实验中独立标定。
    m = 1.0;
    cd = 1e-5;
    cf = 1e-3;
    g = 9.81;
    d = 0.3;
    J << 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0;

    // 【配套实现】X形机架在x、y方向的投影臂长为d/√2。
    // 旋翼1(+x,+y)、2(-x,+y)、3(-x,-y)、4(+x,-y)，偏航符号为+、-、+、-。
    const double arm = d / std::sqrt(2.0);
    Eigen::Matrix4d allocation;
    allocation << cf, cf, cf, cf, arm * cf, arm * cf, -arm * cf, -arm * cf, -arm * cf, arm * cf,
        arm * cf, -arm * cf, cd, -cd, cd, -cd;
    // 矩阵四行依次对应总推力和x、y、z轴力矩；只在构造时求逆。
    F2W = allocation.inverse();
    x.setZero();
    v.setZero();
    R.setIdentity();
    omega.setZero();
    xd.setZero();
    vd.setZero();
    ad.setZero();
    yawd = 0.0;
  }

  void onDesiredState(const trajectory_msgs::MultiDOFJointTrajectoryPoint &des_state) {

    // 【实验要求补充 03｜PART 3.1：读取目标平移状态】
    // 先检查数组非空，再读取目标位置xd、速度vd和加速度ad。
    if (des_state.transforms.empty() || des_state.velocities.empty() ||
        des_state.accelerations.empty())
      return;
    const auto &position = des_state.transforms[0].translation;
    const auto &velocity = des_state.velocities[0].linear;
    const auto &acceleration = des_state.accelerations[0].linear;
    xd << position.x, position.y, position.z;
    vd << velocity.x, velocity.y, velocity.z;
    ad << acceleration.x, acceleration.y, acceleration.z;
    // 【实验要求补充 04｜PART 3.2：读取目标朝向】
    // 检查并归一化四元数，提取目标偏航角yawd，确认目标数据有效。
    const auto &q = des_state.transforms[0].rotation;
    const double norm2 = q.x * q.x + q.y * q.y + q.z * q.z + q.w * q.w;
    if (!std::isfinite(norm2) || norm2 < 1e-12)
      return;
    tf2::Quaternion quat(q.x, q.y, q.z, q.w);
    quat.normalize();
    yawd = tf2::getYaw(quat);
    have_desired = xd.allFinite() && vd.allFinite() && ad.allFinite() && std::isfinite(yawd);
  }

  void onCurrentState(const nav_msgs::Odometry &cur_state) {
    // 【实验要求补充 05｜PART 4：读取实际状态】
    // 读取位置、速度和姿态；把桥接提供的世界系角速度转到机体系。
    const auto &position = cur_state.pose.pose.position;
    const auto &velocity = cur_state.twist.twist.linear;
    const auto &q = cur_state.pose.pose.orientation;
    Eigen::Quaterniond quat(q.w, q.x, q.y, q.z);
    if (!std::isfinite(quat.squaredNorm()) || quat.norm() < 1e-6)
      return;
    quat.normalize();
    R = quat.toRotationMatrix();
    x << position.x, position.y, position.z;
    v << velocity.x, velocity.y, velocity.z;
    const auto &rate = cur_state.twist.twist.angular;
    // 本实验桥接的角速度在世界系中；力矩公式使用机体系角速度。
    omega = R.transpose() * Eigen::Vector3d(rate.x, rate.y, rate.z);
    have_current = x.allFinite() && v.allFinite() && R.allFinite() && omega.allFinite();
  }

  void controlLoop(const ros::TimerEvent &t) {
    Eigen::Vector3d ex, ev, er, eomega;

    // 【实验要求补充 06｜PART 5.1：计算位置和速度误差】
    // 等待两类有效状态，以实际值减目标值，得到ex和ev。
    if (!have_current || !have_desired) {
      ROS_WARN_THROTTLE(2.0, "Waiting for valid current and desired states.");
      return;
    }
    ex = x - xd;
    ev = v - vd;

    // 【实验要求补充 07｜PART 5.2：构造期望姿态】
    // 根据误差求合力，确定机身z轴，再结合目标朝向构造Rd。
    // 世界系z轴向上，+m*g*e3用于抵消重力；位置与速度项采用负反馈。
    const Eigen::Vector3d force = -kx * ex - kv * ev + m * g * e3 + m * ad;
    if (!force.allFinite() || force.norm() < 1e-6)
      return;
    // 合力给出期望推力方向；先检查非零，才能安全归一化。
    const Eigen::Vector3d b3d = force.normalized();
    const Eigen::Vector3d heading(std::cos(yawd), std::sin(yawd), 0.0);
    Eigen::Vector3d b2d = b3d.cross(heading);
    if (b2d.norm() < 1e-6)
      return;
    b2d.normalize();
    const Eigen::Vector3d b1d = b2d.cross(b3d);
    Eigen::Matrix3d Rd;
    Rd.col(0) = b1d;
    Rd.col(1) = b2d;
    Rd.col(2) = b3d;
    // 【实验要求补充 08｜PART 5.3：计算姿态与角速度误差】
    // 用旋转矩阵计算姿态误差；按题目允许的简化省略目标角速度前馈。
    er = 0.5 * Vee(Rd.transpose() * R - R.transpose() * Rd);
    eomega = omega;

    // 【实验要求补充 09｜PART 5.4：计算推力与力矩】
    // 把合力投影到当前机身z轴得到推力，结合姿态和角速度反馈求力矩。
    // 推力是期望合力沿当前机身z轴的投影，不是直接取合力大小。
    const double thrust = force.dot(R.col(2));
    const Eigen::Vector3d moment = -kr * er - komega * eomega + omega.cross(J * omega);
    Eigen::Vector4d wrench;
    wrench << thrust, moment.x(), moment.y(), moment.z();

    // 【实验要求补充 10｜PART 5.5：分配四个旋翼的作用量】
    // 用预先求好的逆分配矩阵，把总推力和三轴力矩换成有符号转速平方。
    // 每个分量表示u_i=ω_i*|ω_i|，不是最终发送的角速度。
    const Eigen::Vector4d rotor_signed_square = F2W * wrench;
    if (!rotor_signed_square.allFinite()) {
      ROS_ERROR_THROTTLE(1.0, "Non-finite rotor command: stop and inspect states.");
      return;
    }
    // 【实验要求补充 11｜PART 5.6：发布旋翼转速】
    // 保留符号开平方，填入4个角速度并发布；单位为rad/s。
    mav_msgs::Actuators command;
    command.header.stamp = ros::Time::now();
    // 发布4个角速度，单位rad/s；不要改成rpm或直接发送平方值。
    command.angular_velocities.resize(4);
    for (int i = 0; i < 4; ++i) {
      command.angular_velocities[i] = signed_sqrt(rotor_signed_square(i));
    }
    rotor_pub.publish(command);
  }
};

// 【程序入口】初始化ROS节点并处理回调，不属于待补全的11处。
int main(int argc, char **argv) {
  ros::init(argc, argv, "controller_node");
  controllerNode n;
  ros::spin();
}
