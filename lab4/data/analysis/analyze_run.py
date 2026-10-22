"""Reproduce ROS1 bag metrics using message-record times and linear interpolation.

Usage: python analyze_run.py --bag ../raw/run_20261022_000059/race.bag --out .
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import numpy as np
from rosbags.highlevel import AnyReader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def yaw(q):
    return np.arctan2(2*(q.w*q.z+q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))


def summarize(error):
    e = np.asarray(error)
    return {'samples': int(len(e)), 'rmse_m': float(np.sqrt(np.mean(e*e))),
            'mean_m': float(np.mean(e)), 'median_m': float(np.median(e)),
            'p95_m': float(np.percentile(e, 95)), 'max_m': float(np.max(e))}


def analyze(bag, out):
    out.mkdir(parents=True, exist_ok=True)
    current, desired, rotor, clocks = [], [], [], []
    gates, counts = [], {}
    with AnyReader([bag]) as reader:
        start, end = reader.start_time / 1e9, reader.end_time / 1e9
        for conn in reader.connections:
            counts[conn.topic] = counts.get(conn.topic, 0) + conn.msgcount
        for conn, stamp, raw in reader.messages():
            msg = reader.deserialize(raw, conn.msgtype)
            t = stamp / 1e9
            if conn.topic == '/current_state':
                p, v, q = msg.pose.pose.position, msg.twist.twist.linear, msg.pose.pose.orientation
                current.append([t, p.x, p.y, p.z, v.x, v.y, v.z, yaw(q)])
            elif conn.topic == '/desired_state' and msg.transforms and msg.velocities:
                tr, v = msg.transforms[0], msg.velocities[0].linear
                tau = msg.time_from_start.sec + msg.time_from_start.nanosec / 1e9
                desired.append([t, tr.translation.x, tr.translation.y, tr.translation.z,
                                v.x, v.y, v.z, yaw(tr.rotation), tau])
            elif conn.topic == '/desired_traj_vertices' and not gates:
                gates = [[p.position.x, p.position.y, p.position.z, float(yaw(p.orientation))]
                         for p in msg.poses]
            elif conn.topic == '/rotor_speed_cmds':
                rotor.append([t, *msg.angular_velocities])
            elif conn.topic == '/clock':
                clocks.append([t, msg.clock.sec + msg.clock.nanosec/1e9])
    a, d, g = np.array(current), np.array(desired), np.array(gates)
    if len(a) < 2 or len(d) < 2:
        raise RuntimeError('Missing state messages')
    assert np.all(np.diff(a[:, 0]) >= 0) and np.all(np.diff(d[:, 0]) >= 0)
    total = float(np.max(d[:, 8]))
    moving = (d[:, 8] > .02) & (d[:, 8] < total-.02)
    origin = float(np.median(d[moving, 0] - d[moving, 8]))
    finish = origin + total
    # Analyze only the trajectory-execution window; do not mix long post-run hover.
    mask = (a[:, 0] >= max(origin, d[0, 0])) & (a[:, 0] <= min(finish, d[-1, 0]))
    fullmask = (a[:, 0] >= d[0, 0]) & (a[:, 0] <= d[-1, 0])
    aligned = np.column_stack([np.interp(a[:, 0], d[:, 0], d[:, j]) for j in range(1, 7)])
    dyaw = np.interp(a[:, 0], d[:, 0], np.unwrap(d[:, 7]))
    err = a[:, 1:4] - aligned[:, :3]
    norm = np.linalg.norm(err, axis=1)
    yawerr = np.arctan2(np.sin(a[:, 7]-dyaw), np.cos(a[:, 7]-dyaw))
    rows = np.column_stack([a[:, 0], a[:, 0]-origin, a[:, 1:4], aligned[:, :3],
                            err, norm, a[:, 7], dyaw, np.rad2deg(yawerr), mask.astype(int)])
    names = ['bag_time_s','trajectory_time_s','actual_x_m','actual_y_m','actual_z_m',
             'desired_x_m','desired_y_m','desired_z_m','error_x_m','error_y_m','error_z_m',
             'position_error_m','actual_yaw_rad','desired_yaw_rad','yaw_error_deg','in_execution']
    np.savetxt(out/'aligned_states.csv', rows, delimiter=',', header=','.join(names), comments='', fmt='%.9f')
    np.savetxt(out/'waypoints.csv', g, delimiter=',', header='x_m,y_m,z_m,yaw_rad', comments='', fmt='%.9f')
    np.savetxt(out/'desired_states.csv', d, delimiter=',',
               header='bag_time_s,x_m,y_m,z_m,vx_mps,vy_mps,vz_mps,yaw_rad,time_from_start_s', comments='', fmt='%.9f')
    # Compare each waypoint in its local time neighborhood. This is a center-distance
    # diagnostic, not an automatic collision detector or gate-passage certification.
    planned_times = []
    last_index = 0
    for gate in g:
        distances = np.linalg.norm(d[last_index:, 1:4]-gate[:3], axis=1)
        index = int(np.argmin(distances)) + last_index
        planned_times.append(float(d[index, 0] - origin))
        last_index = index
    gate_rows = []
    for i, gate in enumerate(g):
        lo = 0 if i == 0 else (planned_times[i-1] + planned_times[i])/2
        hi = total if i == len(g)-1 else (planned_times[i] + planned_times[i+1])/2
        ix = np.flatnonzero(mask & (a[:, 0]-origin >= lo) & (a[:, 0]-origin <= hi))
        if not len(ix):
            raise RuntimeError('No samples near waypoint')
        best = ix[np.argmin(np.linalg.norm(a[ix, 1:4] - gate[:3], axis=1))]
        gate_rows.append([i+1, *gate[:3], planned_times[i], a[best, 0]-origin,
                          np.linalg.norm(a[best, 1:4] - gate[:3])])
    with (out/'waypoint_center_distances.csv').open('w', newline='', encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['waypoint','x_m','y_m','z_m','planned_time_s','nearest_actual_time_s','nearest_center_distance_m']);w.writerows(gate_rows)
    metrics = {
        'run_id': bag.parent.name,
        'bag_sha256': hashlib.sha256(bag.read_bytes()).hexdigest(),
        'bag_start_s': start, 'bag_end_s': end, 'bag_duration_s': end-start,
        'topic_counts': counts, 'waypoint_count': len(g),
        'trajectory_start_estimate_s': origin, 'planned_trajectory_duration_s': total,
        'trajectory_end_estimate_s': finish, 'max_tau_plateau_samples': int(np.sum(np.isclose(d[:,8],total,atol=1e-7))),
        'execution': summarize(norm[mask]), 'all_overlap': summarize(norm[fullmask]),
        'execution_axis_rmse_m': np.sqrt(np.mean(err[mask]**2,axis=0)).tolist(),
        'execution_axis_mean_error_m': np.mean(err[mask],axis=0).tolist(),
        'execution_yaw_rmse_deg': float(np.sqrt(np.mean(np.rad2deg(yawerr[mask])**2))),
        'execution_max_speed_mps': float(np.max(np.linalg.norm(a[mask,4:7],axis=1))),
        'execution_mean_speed_mps': float(np.mean(np.linalg.norm(a[mask,4:7],axis=1))),
        'execution_distance_m': float(np.sum(np.linalg.norm(np.diff(a[mask,1:4],axis=0),axis=1))),
        'endpoint_error_m': float(norm[np.flatnonzero(mask)[-1]]),
        'nearest_center_distances_m': [float(x[-1]) for x in gate_rows],
        'state_rate_hz': float(1/np.median(np.diff(a[:,0]))),
        'desired_rate_hz': float(1/np.median(np.diff(d[:,0]))),
        'clock_backsteps': int(np.sum(np.diff(np.array(clocks)[:,1]) < 0)),
        'method': 'ROS bag record timestamps; desired positions/velocities and unwrapped yaw linearly interpolated to actual-state timestamps; execution origin median(t_record - time_from_start) over advancing samples; execution window excludes final hold; 3D error sqrt(dx²+dy²+dz²).',
        'limits': 'One recorded complete run; planned duration is not independently adjudicated race time. Waypoint center distance does not prove gate passage. Video is checked separately. No fastest-team or acceleration comparison claim.'
    }
    (out/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    plt.rcParams.update({'font.size':10, 'axes.spines.top':False, 'axes.spines.right':False})
    tt = a[mask,0]-origin
    fig,axes=plt.subplots(3,1,figsize=(10,6.4),sharex=True)
    for j,ax in enumerate(axes):
        ax.plot(tt,aligned[mask,j],color='#d97706',ls='--',lw=1.6,label='Desired')
        ax.plot(tt,a[mask,j+1],color='#176b87',lw=1,label='Actual')
        ax.set_ylabel('XYZ'[j]+' (m)');ax.grid(alpha=.2)
    axes[0].legend(ncol=2);axes[-1].set_xlabel('Trajectory execution time (s)')
    fig.tight_layout();fig.savefig(out/'position_tracking.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(10,5.5),sharex=True)
    axes[0].plot(tt,norm[mask],color='#176b87');axes[0].set_ylabel('3D error (m)')
    for j in range(3):axes[1].plot(tt,err[mask,j],label='XYZ'[j],lw=1)
    axes[1].legend(ncol=3);axes[1].set_ylabel('Axis error (m)');axes[1].set_xlabel('Trajectory execution time (s)')
    for ax in axes:ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(out/'tracking_error.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,6))
    ax.plot(d[:,1],d[:,2],ls='--',color='#d97706',label='Desired',lw=1.6)
    ax.plot(a[mask,1],a[mask,2],color='#176b87',label='Actual',lw=1)
    ax.scatter(g[:,0],g[:,1],marker='s',s=28,color='#a42137',label='Waypoint centers')
    for i,gate in enumerate(g):ax.annotate(str(i+1),(gate[0],gate[1]),xytext=(4,4),textcoords='offset points',fontsize=8)
    ax.set(xlabel='X (m)',ylabel='Y (m)',title='Drone racing: desired and actual XY paths');ax.axis('equal');ax.grid(alpha=.2);ax.legend()
    fig.tight_layout();fig.savefig(out/'trajectory_xy.png',dpi=180);plt.close(fig)
    fig=plt.figure(figsize=(9,6));ax=fig.add_subplot(projection='3d')
    ax.plot(d[:,1],d[:,2],d[:,3],ls='--',color='#d97706',label='Desired')
    ax.plot(a[mask,1],a[mask,2],a[mask,3],color='#176b87',lw=1,label='Actual')
    ax.scatter(g[:,0],g[:,1],g[:,2],c='#a42137',marker='s',label='Waypoint centers')
    ax.set(xlabel='X (m)',ylabel='Y (m)',zlabel='Z (m)');ax.legend();fig.tight_layout();fig.savefig(out/'trajectory_3d.png',dpi=180);plt.close(fig)
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    return metrics


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bag',type=Path,default=Path(__file__).resolve().parents[1]/'raw/run_20261022_000059/race.bag');ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
    args=ap.parse_args();analyze(args.bag,args.out)
