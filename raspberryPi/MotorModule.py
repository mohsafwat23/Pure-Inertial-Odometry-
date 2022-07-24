import RPi.GPIO as GPIO #control the gpio pins
from time import sleep
#from picamera import PiCamera

#camera = PiCamera()



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    """Create motor object"""
    def __init__(self, Ena, In1a, In2a, Enb, In1b, In2b):
        #(23,24,25,17,22,27)
        self.Ena = Ena
        self.In1a = In1a
        self.In2a = In2a
        self.Enb = Enb
        self.In1b = In1b
        self.In2b = In2b
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1a, GPIO.OUT)
        GPIO.setup(self.In2a, GPIO.OUT)
        GPIO.setup(self.Enb, GPIO.OUT)
        GPIO.setup(self.In1b, GPIO.OUT)
        GPIO.setup(self.In2b, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.Ena,100) #pulse-width modulation for speed, 100 hz
        self.pwmA.start(0)   #start at 0 hz
        self.pwmB = GPIO.PWM(self.Enb,100) #pulse-width modulation for speed, 100 hz
        self.pwmB.start(0)

    def moveForward(self, speed=0.50, direction=0, t=0):
        speed *= 100 #normalize
        direction *= 100 #normalize
        leftSpeed = speed - direction
        rightSpeed = speed + direction
        if leftSpeed >100: 
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed <-100:
            rightSpeed = -100
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        if leftSpeed < 0:
            GPIO.output(self.In1a, GPIO.HIGH)
            GPIO.output(self.In2a, GPIO.LOW)
        else:
            GPIO.output(self.In1a, GPIO.LOW)
            GPIO.output(self.In2a, GPIO.HIGH)
        if rightSpeed < 0:
            GPIO.output(self.In1b, GPIO.HIGH)  
            GPIO.output(self.In2b, GPIO.LOW)
        else:
            GPIO.output(self.In1b, GPIO.LOW)
            GPIO.output(self.In2b, GPIO.HIGH)
        sleep(t)

    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)

if __name__ == '__main__':
    #camera.start_preview()
    motor = Motor(23,24,25,17,22,27) #initialize motor at the following GPIOs
    motor.moveForward(0.3,0.2,1)
    motor.stop()


