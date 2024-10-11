YOLOv8 Bicep Curl Counter using Pose Estimation
Project Overview
This project implements a real-time bicep curl counter using the YOLOv8 pose estimation model from Ultralytics. 
The model detects key body landmarks (shoulder, elbow, and wrist) to calculate the angles of the arms during exercise, enabling the counting of bicep curls. The project leverages OpenCV for video processing,
NumPy for vector mathematics, and cvzone for overlaying text and visual elements on the video feed.


Table of Contents
Installation
Usage
Features
How It Works
Project Structure
Dependencies
Customization
License


Installation
Clone the Repository
Open your terminal and run:
git clone <repository_url>

Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the dependencies
pip install -r requirements.txt

Usage
Run the Program
After setting up the environment, execute the script by running:
python bicep_curl_counter.py

Feed Video for Detection
The script uses OpenCV to load a video file (curl.mp4) and perform pose estimation in real-time.

Features
Pose Detection: Detects the human body landmarks (key points) such as wrist, elbow, and shoulder using YOLOv8 pose estimation.
Angle Calculation: Calculates the angle formed between the wrist, elbow, and shoulder to track arm movements.
Curl Counting: Counts both left and right bicep curls based on the arm's flexion and extension angles.
Visual Feedback: Displays the detected key points and angles on the screen in real-time.
Direction Detection: Detects when the arm is fully extended or flexed to ensure accurate curl counting.
How It Works
Pose Estimation using YOLOv8
The model identifies key body parts involved in the bicep curl:

Wrist
Elbow
Shoulder
For each frame, it calculates the angle formed by the points:

Vector math is applied to find the angles using NumPy arrays.
The angle is used to determine if the arm is flexing or extending, tracking the curl count based on this information.
Curl Counting Logic
A bicep curl is counted when:
The elbow angle flexes (≥100°) and then extends (≤70°).
The direction_L or direction_R variables track whether the arm is moving up or down.
The counter increases by 0.5 during each phase (upward and downward movement), totaling one full curl per cycle.

Dependencies
Ultralytics YOLOv8: The YOLOv8 model for pose detection.
OpenCV: For video capture and image processing.
NumPy: For vector operations and angle calculations.
cvzone: For easy overlaying of visual elements like text and rectangles on video frames.

Customization
Model: You can switch to a different YOLOv8 pose model by changing the model path in the script:
python
model = YOLO('path_to_model.pt')

Angle Thresholds: Modify the angle thresholds for curl counting to suit other exercises:

if left_Hand_Angle >= 100:  # Flexion angle
   
if left_Hand_Angle <= 70:   # Extension angle
  
License
This project is licensed under the MIT License. Feel free to modify and distribute the project as needed.

