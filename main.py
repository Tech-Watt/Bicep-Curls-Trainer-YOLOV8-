from ultralytics import YOLO
import cv2
import cvzone
import numpy as np


cap = cv2.VideoCapture('curl.mp4')
model = YOLO('yolov8s-pose.pt')


class Angles:

    def __init__(self, p1, p2, p3):
        self.point_one = p1
        self.point_two = p2
        self.point_three = p3

    def unpackAngles(self):
        self.x, self.y, self.z = self.point_one
        self.x1, self.y1, self.z1 = self.point_two
        self.x2, self.y2, self.z2 = self.point_three

    def findAngles(self):
        self.unpackAngles()
        v1 = np.array([self.x, self.y]) - np.array([self.x1, self.y1])
        v2 = np.array([self.x2, self.y2]) - np.array([self.x1, self.y1])

        angle_rad = np.arccos(
            np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        angle_deg = np.degrees(angle_rad)

        try:
            return int(angle_deg)
        except:
            pass

    def drawPointCircles(self):
        cv2.circle(frame, (int(self.x), int(self.y)), 8, (0, 255, 0), -1)
        cv2.circle(frame, (int(self.x), int(self.y)), 12, (0, 255, 255), 6)
        cv2.circle(frame, (int(self.x), int(self.y)), 16, (0, 0, 255), 6)

        cv2.circle(frame, (int(self.x1), int(self.y1)), 8, (0, 255, 0), -1)
        cv2.circle(frame, (int(self.x1), int(self.y1)), 12, (0, 255, 255), 6)
        cv2.circle(frame, (int(self.x1), int(self.y1)), 16, (0, 0, 255), 6)

        cv2.circle(frame, (int(self.x2), int(self.y2)), 8, (0, 255, 0), -1)
        cv2.circle(frame, (int(self.x2), int(self.y2)), 12, (0, 255, 255), 6)
        cv2.circle(frame, (int(self.x2), int(self.y2)), 16, (0, 0, 255), 6)

    def drawAngleLine(self):
        color = (90, 200, 66)
        cv2.line(frame, (int(self.x), int(self.y)),
                 (int(self.x1), int(self.y1)), color, 6)
        cv2.line(frame, (int(self.x1), int(self.y1)),
                 (int(self.x2), int(self.y2)), color, 6)
        cv2.line(frame, (int(self.x2), int(self.y2)),
                 (int(self.x), int(self.y)), color, 6)


counter_L = 0
direction_L = 0

counter_R = 0
direction_R = 0

while True:

    rt, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    
    result = model(frame)
    # frame = result[0].plot()
    keypoints = result[0].keypoints.data[0]

    right_wrist = keypoints[10]
    right_elbow = keypoints[8]
    right_shoulder = keypoints[6]

    left_wrist = keypoints[9]
    left_elbow = keypoints[7]
    left_shoulder = keypoints[5]

    left_angle = Angles(p1=left_wrist, p2=left_elbow, p3=left_shoulder)
    left_Hand_Angle = left_angle.findAngles()
    left_angle.drawPointCircles()
    left_angle.drawAngleLine()

    right_angle = Angles(p1=right_wrist, p2=right_elbow, p3=right_shoulder)
    right_Hand_Angle = right_angle.findAngles()
    right_angle.drawPointCircles()
    right_angle.drawAngleLine()

    try:
        if left_Hand_Angle >= 100:
            if direction_L == 0:
                counter_L += 0.5
                direction_L = 1

        if left_Hand_Angle <= 70:
            if direction_L == 1:
                counter_L += 0.5
                direction_L = 0
    except:
        pass

    try:
        if right_Hand_Angle >= 100:
            if direction_R == 0:
                counter_R += 0.5
                direction_R = 1

        if right_Hand_Angle <= 70:
            if direction_R == 1:
                counter_R += 0.5
                direction_R = 0
    except:
        pass

    cvzone.putTextRect(frame, f'<L :{left_Hand_Angle}', [
                       11, 33], border=2, scale=2)
    cvzone.putTextRect(frame, f'LC: {int(counter_L)}', [
                       11, 117], border=2, scale=2)

    cvzone.putTextRect(frame, f'<R :{right_Hand_Angle}', [
                       11, 75], border=2, scale=2)
    cvzone.putTextRect(frame, f'RC: {int(counter_R)}', [
        11, 159], border=2, scale=2)
    
    cvzone.putTextRect(frame, f'YOLOV8 Pose', [411, 33], border=1, scale=2)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
