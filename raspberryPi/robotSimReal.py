import math,sys
import pygame
from pygame.locals import *
import time 
import torch
from models.NNmodel import NN
import numpy as np
import board
import adafruit_bno055
from MotorModule import Motor

# Initiate motor, IMU, and calibrate IMU
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

#exit game if window is closed
def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

#import model
model = NN(6, 100, 16, 2)
model.load_state_dict(torch.load("./3.model.pth"))

#create window
w,h = 720,720
pygame.init()
CLOCK = pygame.time.Clock()
FPS = 120
screen = pygame.display.set_mode((w,h))
center = screen.get_rect().center
pygame.display.set_caption("Robot Game")

#Colors
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Initate robot parameters
RobotX,RobotY = center#w/2,h/2 #Robot position at center 
dx,dy = 0.0,0.0 #Robot movement
i = 0

#Robot gains (make it move in a straight path)
beta = 0.001
beta2 = 0.01
angle_init = sensor.euler[0]

while True:
    events()
    try:
        angle = sensor.euler[0] - angle_init
        if angle is not None:
            if angle > 180:
                angle = angle - 360
            if angle > 0:
                robot.moveForward(0.25, beta*angle, 0.005)
            else:
                robot.moveForward(0.25, beta2*angle,0.005)
        X = torch.tensor([
            sensor.acceleration[0], sensor.acceleration[1], sensor.acceleration[2],
            sensor.gyro[0], sensor.gyro[1], sensor.gyro[2]
            ])
        predicted = model(X).detach()
        dx = predicted[0].item()*500.
        dy = predicted[1].item()*500.
        RobotX += dx
        RobotY += dy
        i += 1
    except KeyboardInterrupt:
        robot.stop()
        break
    pygame.draw.circle(screen,BLUE,(int(RobotX),int(RobotY)),25,0)
    #pygame.draw.line(screen,RED,(dxPrev, dyPrev),(int(RobotX),int(RobotY)))
    pygame.display.update()
    CLOCK.tick(FPS)
    screen.fill(WHITE)
    #time.sleep(0.1)