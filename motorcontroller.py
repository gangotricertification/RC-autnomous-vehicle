import cv2
import RPi.GPIO as gpio
import time
import numpy as np
from direction import prepro


gpio.setmode(gpio.BOARD)

gpio.setup(7,gpio.OUT)
gpio.setup(12,gpio.OUT)

gpio.setup(11,gpio.OUT)  #white    #reverse left
gpio.setup(15,gpio.OUT)  #grey     #forward right
gpio.setup(18,gpio.OUT)  #blue     #forward left
gpio.setup(16,gpio.OUT)  #red      #reverse left

r = gpio.PWM(7,100)
l = gpio.PWM(12,100)

start = time.time()
cap = cv2.VideoCapture(0)
while(True):
    ret,frame = cap.read()
    a = prepro(frame)
    
    direction = a[0]
    angle = a[1]


    gpio.output(11,False)
    gpio.output(15,True)
    gpio.output(18,True)
    gpio.output(16,False)

    l.start(100)
    r.start(100)
    
    if angle > 5 and angle <= 10 and direction == "left":
        print("Soft Left")
        l.ChangeDutyCycle(0.5*100)
        r.ChangeDutyCycle(1*100)
    elif angle > 5 and angle <= 10 and direction == "right":
        print("Soft Right")
        l.ChangeDutyCycle(1*100)
        r.ChangeDutyCycle(0.5*100)
    elif angle > 10 and direction == "left":
        print("Hard Left")
        l.ChangeDutyCycle(0*100)
        r.ChangeDutyCycle(1*100)
    elif angle > 10 and direction == "right":
        print("Hard right")
        l.ChangeDutyCycle(1*100)
        r.ChangeDutyCycle(0*100)
    else:
        print(" Go straight")
    end = time.time()
    if end-start >= 30:
        break
gpio.cleanup()
