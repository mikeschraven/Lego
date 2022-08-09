# TODO: Space bar => All stop
# Bug: initial duty cycle sometimes 0%
# Improvement: initial duty cycle 60% not enough 

import time
import curses
from sys import exit
import RPi.GPIO as GPIO
from dc_motor import DcMotor

SPEED_STEP = 1
LEFT_MOTOR_CCW_PIN = 22
LEFT_MOTOR_CW_PIN = 23
RIGHT_MOTOR_CCW_PIN = 17
RIGHT_MOTOR_CW_PIN = 18

_leftMotor = DcMotor('left', LEFT_MOTOR_CCW_PIN, LEFT_MOTOR_CW_PIN)
_rightMotor = DcMotor('right', RIGHT_MOTOR_CCW_PIN, RIGHT_MOTOR_CW_PIN)

def moveMotor(leftMotor = True, cw = True):   
    (_leftMotor if leftMotor else _rightMotor).move(cw)

def stopMotor(leftMotor = True):
    (_leftMotor if leftMotor else _rightMotor).stop()

def changeMotorSpeed(leftMotor = True, step = 1):
  (_leftMotor if leftMotor else _rightMotor).changeSpeed(step)


#                  Left Motor        Right Motor
#  CW Direction        D                  L
#  Stop                S                  K
#  CCW Direction       A                  J
#  Increase Speed      W                  I
#  Decrease Speed      X                  M
#  Quit                        Escape  

shell = curses.initscr()
shell.nodelay(False)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
_leftMotor.setup()
_rightMotor.setup()

while True:
    key = shell.getch()
    if key == 97: # A key
        moveMotor(True, False)
    elif key == 100: # D key
        moveMotor(True, True)
    elif key == 105: # I key
        changeMotorSpeed(False, SPEED_STEP)
    elif key == 106: # J key
        moveMotor(False, False)        
    elif key == 107: # K key
        stopMotor(False)
    elif key == 108: # L key
        moveMotor(False, True)
    elif key == 109: # M key
        changeMotorSpeed(False, -SPEED_STEP)
    elif key == 115: # S key 
        stopMotor(True)  
    elif key == 119: # W key
        changeMotorSpeed(True, SPEED_STEP)
    elif key == 120: # X key
        changeMotorSpeed(True, -SPEED_STEP)
    elif key == 27: # Escape key
        curses.endwin()
        exit(0)
