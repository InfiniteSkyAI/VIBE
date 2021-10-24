
import joblib
import numpy as np
import os
from scipy.spatial.transform import Rotation as R
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', type=str, default='output/sample_video/vibe_output.pkl')
parser.add_argument('--output_folder', type=str, default='processed_output')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--output_joint_format', type=str, default='quat')
args = parser.parse_args()

"""
Example usage with VIBE module:
python test/sim/smpl_matching_humanoid.py --input_traj ../VIBE/processed_output/mujoco_shaped_smpl_pose.npy -v
"""

#Current mapping. Should be dynamically passed later on
mapping_smpl2mujoco = {
    0: 0, #left hip 
    1: 3, #left knee
    2: 6, #left ankle
    3: 1, #right hip 
    4: 4, #right knee
    5: 7, #right ankle
    6: 2, #lower spine
    7: 5, #upper spine
    8: 12, #left clavicle
    9: 15, #left shoulder
    10: 17, #l elbow
    11: 19, #l wrist
    12: 13, #right clavicle
    13: 16, #right shoulder
    14: 18, #r elbow
    15: 20 #r wrist
}

"""
Skipped things
8 spine 3
9 left toes
10 right toes
11 neck
14 head
"""

data = joblib.load(args.input_folder)[1]['pose']

#Set shape to be in euler for the sake of Mujoco
if args.output_joint_format == 'euler':
    data_shape = (data.shape[0], 16*3, 1)
#if args.output_joint_format == 'quat':
else:
    data_shape = (data.shape[0], 16, 4)

mujoco_shaped_pose = np.zeros(data_shape)

frame_num = 0
for d in range(data.shape[0]):

    if args.verbose:
        print("File: ", d)

    #params = dict(zip((k for k in data), (data[k] for k in data)))
    smpl_pose = data[frame_num].reshape(24,3)[1:22]
    mujoco_pose = np.zeros(data_shape[1:3])

    for k, v in mapping_smpl2mujoco.items():

        rot_vec = smpl_pose[v]
        if args.verbose:
            print(f"adding to ind {k}:", rot_vec)

        #Rotate axes to match mujoco
        x_orig, y_orig, z_orig = rot_vec
        new_vec = [x_orig, -z_orig, y_orig]

        #Convert angle axis to mujoco style quaternion idendity = (1, 0, 0, 0)
        rotation = R.from_rotvec(new_vec)
        
        if v == 5:
            rot_vec = smpl_pose[8]
            if args.verbose:
                print(f"adding to ind {k}:", rot_vec)

            #Rotate axes to match mujoco
            x_orig, y_orig, z_orig = rot_vec
            new_vec = [x_orig, -z_orig, y_orig]
            top_spine_rotation = R.from_rotvec(new_vec)
            rotation = top_spine_rotation * rotation

        if args.output_joint_format == 'euler':
            start_ind = k*3
            euler_data = rotation.as_euler
        #if args.output_joint_format == 'quat':
        else:
            mujoco_pose[k] = np.roll(rotation.as_quat(), 1)


    if args.verbose:
        print(mujoco_pose)
    mujoco_shaped_pose[frame_num] = mujoco_pose
    frame_num += 1

np.save(f"{args.output_folder}/mujoco_shaped_smpl_pose.npy", mujoco_shaped_pose)