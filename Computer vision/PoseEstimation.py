import cv2
import mediapipe as mp
import time
import math
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import os
import serial.tools.list_ports
import data_com_read_both

ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    print(port)
    print(desc)
    print(hwid)
    if desc.find("USB-SERIAL CH340") != -1:
        esp_server = port
    # if desc.find("Silicon Labs CP210x USB to UART Bridge") != -1:
    #     esp_client = port

serialPort = serial.Serial(port = esp_server, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle
        # print(angle)
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

def main():
    pointCoor = pd.DataFrame()
    angle_data = pd.DataFrame()
    real_time = pd.DataFrame()

    cap = cv2.VideoCapture("https://192.168.134.85:8080/video")
    # cap = cv2.VideoCapture('Videos/punch1.mp4')
    # cap = cv2.VideoCapture(0)
    cTime_0 = time.time()

    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        # img = cv2.flip(img, 1)
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        cTime = time.time() - cTime_0
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)

        if len(lmList) != 0 and serialPort.in_waiting > 0:
            print(lmList[14], '--', type(lmList[14][1]))
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 15, (0, 0, 255), cv2.FILLED)
            arm_angle = detector.findAngle(img, 12, 14, 16)
            wrist_angle = detector.findAngle(img, 14, 16, 18)
            shoulder_angle = detector.findAngle(img, 14, 12, 24)
            joint_list = lmList[14] + list([arm_angle]) + lmList[16] + list([wrist_angle]) + lmList[12] + list(
                [shoulder_angle]) + list([cTime])
            pointCoor = pd.concat([pointCoor, pd.Series(joint_list)], axis=1)

            serialString = serialPort.readline()
            print(serialString.decode('ASCII'))
            x = list([serialString.decode('Ascii')])
            angle_data = pd.concat([angle_data, pd.Series(x)], axis=1)

            real_time = pd.concat([real_time, pd.Series(cTime)], axis=1)

        # if (serialPort.in_waiting > 0):
        #     # Read data out of the buffer until a carraige return / new line is found
        #     serialString = serialPort.readline()
        #     print(serialString.decode('ASCII'))
        #     x = list([serialString.decode('Ascii')])
        #     angle_data = pd.concat([angle_data, pd.Series(x)], axis=1)

        if cTime > 3:
        # if cv2.waitKey(1) & 0xFF == ord('d'):
            break
    pointCoor = pointCoor.T
    pointCoor.columns = ['14', 'arm_x', 'arm_y', 'arm_angle', '16', 'wrist_x', 'wrist_y', 'wrist_angle', '12','shoulder_x', 'shoulder_y', 'shoulder_angle', 'time']
    pointCoor.to_csv("Data Record/final_ex_1.csv", index=None, header=True)

    angle_data = angle_data.T
    angle_data.to_csv("Data Record/final_com_1.csv", index=None, header=True)

    real_time = real_time.T
    real_time.to_csv("Data Record/final_real_time.csv", index=None, header=True)

if __name__ == "__main__":
    main()

    # df2 = pd.read_csv("Data Record/com_1.csv")
    # print(df2.describe())

    df_mpu, df_loadcell = data_com_read_both.extract_data("Data Record/final_com_1.csv","Data Record/final_real_time.csv")

    df = pd.read_csv('Data Record/final_ex_1.csv')
    print(df.describe())
    print(df.head())

    fig = plt.figure(figsize=(14,7))
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)

    ax1.plot(df['time'], df['arm_angle'])
    ax1.plot(df['time'][0], 0)
    ax1.plot(df['time'][0], 180)
    ax1.title.set_text('Arm')

    ax2.plot(df['time'], df['wrist_angle'])
    ax2.plot(df['time'][0], 0)
    ax2.plot(df['time'][0], 180)
    ax2.title.set_text('Wrist')

    ax3.plot(df['time'], df['shoulder_angle'])
    ax3.plot(df['time'][0], 0)
    ax3.plot(df['time'][0], 180)
    ax3.title.set_text('Shoulder')

    ax4.plot(df_mpu['time'], df_mpu['z'])
    ax4.plot(0, 0)
    ax4.plot(0, 180)

    ax5.plot(df_loadcell['time'],df_loadcell['force'])
    ax5.plot(0, 0)
    ax5.plot(0, 5)

    plt.show()