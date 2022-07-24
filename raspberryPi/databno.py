import board
import adafruit_bno055
import time
from MotorModule import Motor
import torch
import numpy as np
#import pandas as pd

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
sensor_not_calibrated = True
# cal_counter = 0
# while sensor_not_calibrated:
#     print(sensor.calibration_status)
#     if(sensor.calibration_status[2] == 3):
#         cal_counter +=1
#         if cal_counter > 10:
#             print(sensor.acceleration)
#             sensor_not_calibrated = False
# for i in range(100):
#     print(sensor.acceleration)
#     time.sleep(0.1)

while True:
    try:
        #if not None in (sensor.acceleration  + sensor.gyro):
        X = np.array([
            sensor.acceleration[0], sensor.acceleration[1], sensor.acceleration[2],
            sensor.gyro[0], sensor.gyro[1], sensor.gyro[2]
            ])
        print(X)
        #if not np.isnan(X).all():
        if not None in X:
            print(torch.tensor(X))
        #print("accX: ",sensor.acceleration[0])
        #print("accY: ",sensor.acceleration[1])
        #print("accZ: ",sensor.acceleration[2])
        #time.sleep(0.5)
    except KeyboardInterrupt:
        break
