import math,sys
import pygame
from pygame.locals import *
import time 
import torch
import torch.nn as nn
from models.NNmodel import NN
import pandas as pd
import numpy as np

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

#import data
df = pd.read_csv('inputData.csv')   # get data as df
X = df.iloc[: , 1:].to_numpy()
nX = np.shape(X)[1]    # input layer
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

RobotX,RobotY = center#w/2,h/2 #Robot position at center 
dx,dy = 0.0,0.0 #Robot movement
totalDistance = 0 #Total distance traveled
speed = 5
i = 0

while True:
    events()
    tensor_X = torch.from_numpy(X[i].astype(np.float32))
    predicted = model(tensor_X).detach()
    dx = predicted[0].item()*500.
    dy = predicted[1].item()*500.
    # if counter > 10:
    #     dxPrev, dyPrev = RobotX, RobotY
    RobotX += dx
    RobotY += dy
    i += 1
    pygame.draw.circle(screen,BLUE,(int(RobotX),int(RobotY)),25,0)
    #pygame.draw.line(screen,RED,(dxPrev, dyPrev),(int(RobotX),int(RobotY)))
    pygame.display.update()
    CLOCK.tick(FPS)
    screen.fill(WHITE)
    time.sleep(0.1)