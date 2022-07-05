import board
import adafruit_bno055
import time
from MotorModule import Motor
import pandas as pd

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
robot = Motor(23,24,25,17,22,27)
sensor_not_calibrated = True
cal_counter = 0
while sensor_not_calibrated:
    print(sensor.calibration_status)
    if(sensor.calibration_status[2] == 3):
        cal_counter +=1
        if cal_counter > 10:
            print(sensor.acceleration)
            sensor_not_calibrated = False
for i in range(250):
    print(sensor.acceleration)
    time.sleep(0.1)

time.sleep(15)
accX = []
accY = []
accZ = []
gyrX = []
gyrY = []
gyrZ = []
t = []
t_init = time.time()
beta = 0.001
beta2 = 0.01
angle_init = sensor.euler[0]
while True:
    try:
        angle = sensor.euler[0] - angle_init
        if angle is not None:
            if angle > 180:
                angle = angle - 360
            if angle > 0:
                robot.moveForward(0.25, beta*angle, 0.005)
            else:
                robot.moveForward(0.25, beta2*angle,0.005)

        accX.append(sensor.acceleration[0])
        accY.append(sensor.acceleration[1])
        accZ.append(sensor.acceleration[2])
        t.append(float(time.time()))
        gyrX.append(sensor.gyro[0])
        gyrY.append(sensor.gyro[1])
        gyrZ.append(sensor.gyro[2])
        
    except KeyboardInterrupt:
        robot.stop()
        break
        #raise
        #sensor

data_dict = {'time':t, 'accX':accX, 'accY':accY, 'accZ':accZ, 'gyrX':gyrX, 'gyrY':gyrY,'gyrZ':gyrZ}
minLen = 1000000000000000000000000000000000000000
for key in data_dict:
    valLen = len(data_dict[key])
    if valLen < minLen:
        minLen = valLen
for key in data_dict:
    data_dict[key] = data_dict[key][:minLen]
df = pd.DataFrame(data_dict)
df.to_csv('data1.csv')