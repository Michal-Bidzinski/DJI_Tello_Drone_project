# DJI_Tello_Drone_project

Follow the face of the drone and create a 3D model of the head. Thanks to the DJI Tello drone and the program located in this repository, it is very simple. The drone uses a camera to send images to the user's computer, where face detection takes place and appropriate control is generated. 

## Face detection
 
A cascade classifier was used for face detection. The implementation from the OpenCV library was used and downloaded a list of features for face detection. During the tests, greater efficiency was achieved in well-lit places. 

## Cloning the repository
To clone the repository use the following lines:
```
git clone https://github.com/Michal-Bidzinski/DJI_Tello_Drone_project.git
cd DJI_Tello_Drone_project
```

Create and activate virtual environment:
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

Install requirements:
```
pip install -r requirements.txt
```
## How to use

1. Turn on the drone.
2. Connect to the drone's WIFI network (after turning on the drone, wait a while before its WIFI network is available).
3. Run the program with the command: 
```
python3 Keyboard_and_FaceTracking_and_Smile.py
```
After a while, a window with a preview from the drone's camera and a window for controlling the drone will appear.
4. Click on the black window to control. 
Now you can use the keyboard to perform the following actions:
- "e" key - take off the drone, the drone takes off and goes up
- "q" key - the drone lands
- "z" key - starting the data collection sequence for the 3D model - the drone flies in a circle around the head, recording a video needed to reconstruct the model
- "x" key - end of data collection sequence 

After the drone has taken off and the desired height is reached, the drone remains in a fixed position until it detects a face. When detected, depending on where it is in the camera image, the drone rotates, moves forward or backward, rises or descends so that the face is in the center of the image and the drone is at the correct distance from the head. PID regulators are used to perform the above-mentioned movements, thanks to which the drone does not make long movements. 


## Notes and warnings

The lap sequence is very sensitive to gusts of wind, so it should be done indoors. In order for the sequence to be performed as accurately as possible, it is worth ensuring a flat surface under the drone. 




