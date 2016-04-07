#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper 
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import Maze
import Cell

###########################################################################
# MAIN
###########################################################################

# create a default object, no changes to I2C address or frequency
shield = Adafruit_MotorHAT()

# Motor Initialization
left = shield.getStepper(200, 1)  	# 200 steps/rev, motor port #1
right = shield.getStepper(200, 2)

left.setSpeed(30)  		# 30 RPM
right.setSpeed(30)  		# 30 RPM

# Remote Sensining Initialization
remote_sensing = RemoteSensing()

# Robot Initialization
scampr = Robot(left, right, remote_sensing)


scampr.start(); 
atexit.register(turnOffMotors)

###########################################################################

class Robot(object):

    def __init__(self, left_motor, right_motor, remote_sensing):
    	print "Initialized Robot!";


class RemoteSensing(object):

	def __init__():
		print "Remotely Sense things";


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	shield.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(4).run(Adafruit_MotorHAT.RELEASE)



#while (True):
#	print("Single coil steps")
#	myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
#	myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)

#	print("Double coil steps")
#	myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)
#	myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
#
#	print("Interleaved coil steps")
#	myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.INTERLEAVE)
#	myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
#
#	print("Microsteps")
#	myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
#	myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
