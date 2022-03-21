Recruitment Task

#3D Pitch Player Pose Estimation

## Problem Definition

Aim of this task is to create a reliable method for 3D pitch player pose estimation.


There are many approaches in current research literature for pose estimation. However, most of those methods estimate a local pose - i.e. the coordinates are in a reference frame local to a particular player. Therefore, transformation of the local pose onto a globally shared pitch space is necessary in order to perform any analysis that uses information about joint player arrangement.


What is more, provided data is not perfect. There may be errors in estimated camera parameters (due to sudden camera movement) or in player joint positions - e.g. during player occlusions. A good solution should try to take this into account.


## Data

### Data given in this tasks is as follows:

camera_smooth.csv: per-frame estimated camera parameters
df_kpt.csv:  2D (on image) player body joint detections
df_pose_local.csv: local 3D player body joint detections
df_pose_global_sample.csv: sample dataframe with 3D pitch player body joints
df_track.csv: information about player tracking & detection
video.mkv: first minute sample of original video
const.py: Python module with body pose constants

###### Description of the camera_smooth.csv columns:

rot_x, rot_y, rot_z: extrinsic camera rotation in Rodrigues format
tx, ty, tz: extrinsic camera translation
fx, fy: intrinsic camera focal lengths
princ_x, princ_y: intrinsic camera principal point coordinates
error: camera measurement error (internal metric)

Important - provided camera parameters assume global pitch space origin is in the top-left corner of the pitch with a 50 units margin. Scale is in decimeters and the Z axis is reverted (with negative values above the pitch plane). For example, a player positioned 5m to the right of the left pitch line and 7m to the bottom of the upper line of the pitch will have (x, y)  coordinates of (100, 120). In addition, camera parameters assume image size of (640, 360), so it has to be scaled accordingly to the provided data and video (that are in 4K).

###### Description of the df_kpt.csv columns:

kx , ky: x and y position of the given joint
score: confidence of joint detection
kid: COCO joint index

###### Description of the df_pose_local.csv columns:

kx , ky, kz: local x, y, z position of the given joint (units are meters, but may have some error)
kid: SPIN joint index

###### Description of the df_pose_global_sample.csv columns:

kx , ky, kz: global pitch space x, y, z position of the given joint
kid: SPIN joint index

###### Description of the df_track.csv columns:

x0, y0: top left bounding box coordinates
x1, y1: bottom right bounding box coordinates
score: confidence of player detection

###### Shared columns description:

file_name: video frame index
detection_id: player detection id, unique across a single frame
track_id: player tracking id, unique across all frames

###### Description of the const.py module:

COCOKpts: COCO keypoint indices
SPINKpts: SPIN keypoint indices
SPIN_TO_COCO: mapping from SPIN to COCO indices - necessary to perform required estimation
COCO_SKELETON: human skeleton based on COCO keypoints
SPIN_SKELETON: human skeleton based on SPIN keypoints

## Task

Your task is to construct and implement a method that estimates a 3D position of each player joint in the global pitch space.


A solution should consist of:

Implementation of the method
Output file

Implementation has to be provided as a Python script or a jupyter notebook and should utilize only the provided datasets (i.e. you can’t run a separate keypoint detection model etc.).


The output file should have the same structure as the provided df_pose_global_sample.csv file. However, it should contain information about all the joints in all frames available in the provided df_pose_local.csv file (you can omit frames where there is no available camera information).


###### What you should take into account:

Your algorithm should have a reasonable runtime (e.g. 1 frame per second)
Final global pitch space joint positions should result in a smooth motion
Resulting body pose motion should be as plausible as possible (e.g. high skew of the pose in a direction perpendicular to the motion is not natural and you may try to combat it)
