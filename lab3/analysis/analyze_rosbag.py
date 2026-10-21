from pathlib import Path
from rosbags.rosbag1 import Reader
from rosbags.typesys import Stores,get_typestore,get_types_from_msg
import numpy as np,json
from scipy.spatial.transform import Rotation
import argparse
parser=argparse.ArgumentParser(description='Analyze Lab3 circular ROSbag tracking errors')
parser.add_argument('bag',type=Path)
parser.add_argument('--output',type=Path,default=Path('recomputed_analysis'))
args=parser.parse_args()
bag=args.bag
out=args.output
out.mkdir(parents=True,exist_ok=True)

store=get_typestore(Stores.ROS1_NOETIC);rows={};meta=[]
with Reader(bag) as reader:
 for c in reader.connections:
  store.register(get_types_from_msg(c.msgdef.data,c.msgtype));meta.append({'topic':c.topic,'type':c.msgtype,'count':c.msgcount})
 for c,t,data in reader.messages():
  m=store.deserialize_ros1(data,c.msgtype);t=t/1e9
  if c.topic=='/current_state':
   p=m.pose.pose.position;q=m.pose.pose.orientation;v=m.twist.twist.linear;w=m.twist.twist.angular
   rows.setdefault('state',[]).append([m.header.stamp.sec+m.header.stamp.nanosec/1e9,t,p.x,p.y,p.z,q.x,q.y,q.z,q.w,v.x,v.y,v.z,w.x,w.y,w.z])
  elif c.topic=='/desired_state':
   p=m.transforms[0].translation;q=m.transforms[0].rotation;v=m.velocities[0].linear
   rows.setdefault('desired',[]).append([t,p.x,p.y,p.z,q.x,q.y,q.z,q.w,v.x,v.y,v.z])
  elif c.topic=='/rotor_speed_cmds':
   rows.setdefault('rotor',[]).append([m.header.stamp.sec+m.header.stamp.nanosec/1e9,t,*m.angular_velocities])
arrays={}
for name,r in rows.items():
 a=np.array(r);a=a[np.argsort(a[:,0],kind='stable')];_,idx=np.unique(a[:,0],return_index=True);a=a[idx];arrays[name]=a;np.save(out/(name+'.npy'),a)
s=arrays['state'];d=arrays['desired'];mask=(s[:,0]>=d[0,0])&(s[:,0]<=d[-1,0]);s=s[mask];t=s[:,0]
ref=np.column_stack([np.interp(t,d[:,0],d[:,j]) for j in (1,2,3)]);err=s[:,2:5]-ref;norm=np.linalg.norm(err,axis=1)
yaw=Rotation.from_quat(s[:,5:9]).as_euler('xyz')[:,2];dyaw=np.unwrap(Rotation.from_quat(d[:,4:8]).as_euler('xyz')[:,2]);ryaw=np.interp(t,d[:,0],dyaw);yawerr=np.arctan2(np.sin(yaw-ryaw),np.cos(yaw-ryaw))
radius=np.linalg.norm(s[:,2:4],axis=1)
metrics={'topics':meta,'time_basis':'state header stamp; desired bag receipt ROS timestamp; linear interpolation; all common-time samples','start_ros_s':float(t[0]),'end_ros_s':float(t[-1]),'duration_s':float(t[-1]-t[0]),'samples':len(t),'rmse_xyz_m':np.sqrt(np.mean(err**2,axis=0)).tolist(),'rmse_position_m':float(np.sqrt(np.mean(norm**2))),'mean_position_error_m':float(np.mean(norm)),'max_position_error_m':float(norm.max()),'p95_position_error_m':float(np.percentile(norm,95)),'mean_z_m':float(s[:,4].mean()),'min_z_m':float(s[:,4].min()),'max_z_m':float(s[:,4].max()),'mean_radius_m':float(radius.mean()),'radial_rmse_m':float(np.sqrt(np.mean((radius-5)**2))),'yaw_rmse_deg':float(np.rad2deg(np.sqrt(np.mean(yawerr**2)))),'rotor_min_rad_s':float(arrays['rotor'][:,2:].min()),'rotor_max_rad_s':float(arrays['rotor'][:,2:].max()),'desired_turns':float(abs(dyaw[-1]-dyaw[0])/(2*np.pi)),'actual_turns':float(abs(np.unwrap(np.arctan2(s[-1:,3],s[-1:,2]))[0]-np.unwrap(np.arctan2(s[:,3],s[:,2]))[0])/(2*np.pi))}
angle=np.unwrap(np.arctan2(s[:,3],s[:,2]));metrics['actual_turns']=float(abs(angle[-1]-angle[0])/(2*np.pi))
np.savez(out/'aligned_data.npz',time=t-t[0],position=s[:,2:5],reference=ref,error=err,norm=norm,yaw_error_deg=np.rad2deg(yawerr),radius=radius)
(out/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
