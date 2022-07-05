import board
import adafruit_bno055
import time
from MotorModule import Motor
import pandas as pd

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
        print(sensor.acceleration)
        print("accX: ",sensor.acceleration[0])
        print("accY: ",sensor.acceleration[1])
        print("accZ: ",sensor.acceleration[2])
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
