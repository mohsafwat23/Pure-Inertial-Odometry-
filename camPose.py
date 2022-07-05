import numpy as np
import cv2
import cv2.aruco as aruco
import csv
import time
#np.load('calibration.pckl', allow_pickle=True)

cameraMatrix = np.load('cameraMatrix.npy')
distCoeffs = np.load('distCoeffs.npy')

cap = cv2.VideoCapture(0)
markerSize = 0.084
f = open("robotPosition.csv", "a+")
writer = csv.writer(f, delimiter=',')
while True:
    _, img = cap.read()
    # img=cv2.resize(img,(w,h))
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Pick the AruCo marker 
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)#DICT_4X4_250)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(imgGray, aruco_dict, parameters=parameters)
    if type(ids) is np.ndarray:
        # pass on the distortion and camera coefficients, and the marker size
        rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, markerSize, cameraMatrix, distCoeffs)
        #cv2.aruco.drawAxis(img, cameraMatrix, distCoeffs, rvecs , tvecs, 0.1)
        t = float(time.time())
        for i, id in enumerate(ids):
            data = [t, i, tvecs[i][0][0], tvecs[i][0][1], tvecs[i][0][2]]
            writer.writerow(data)
    f.flush()
    cv2.imshow("Output",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

