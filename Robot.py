#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper 
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import threading
import time
import atexit
import Maze
import Cell

###########################################################################
# MAIN
###########################################################################

# create a default object, no changes to I2C address or frequency
shield = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
threadL = threading.Thread()
threadR = threading.Thread()

# Motor Initialization
left = shield.getStepper(200, 1)  	# 200 steps/rev, motor port #1
right = shield.getStepper(200, 2)

left.setSpeed(30)  			# 30 RPM
right.setSpeed(30)  		# 30 RPM
step_style = Adafruit_MotorHAT.INTERLEAVE

# Remote Sensining Initialization
remote_sensing = RemoteSensing()

# Robot Initialization
scampr = Robot(left, right, remote_sensing)


scampr.start(); 
atexit.register(turnOffMotors)

###########################################################################

class Robot(object):

    __init__(self, left_motor, right_motor, remote_sensing):
        self.row = 0 
        self.col = 0 
        self.maze = [[Cell() for x in range(16)] for x in range(16)]; 
        self.current_direction = "E";

    def isSolved(self): 
        return (row == 7 or row == 8) and (col == 7 or col == 8)    

    def isVisited():
        return self.maze[row][col].visited; 
    
    def isWall(direction):
        return self.maze[row][col].walls[direction]; 

    def stepForward(steps):
    	threadL = threading.Thread(target=stepper_worker, args=(left, steps, Adafruit_MotorHAT.FORWARD, step_style))
		threadR = threading.Thread(target=stepper_worker, args=(right, steps, Adafruit_MotorHAT.FORWARD, step_style))
		threadL.start()
    	threadR.start()

   	def rotate(cw, steps):
   		left_dir = Adafruit_MotorHAT.FORWARD
   		right_dir = Adafruit_MotorHAT.BACKWARD
   		if (not cw):
   			left_dir = Adafruit_MotorHAT.BACKWARD
   			right_dir = Adafruit_MotorHAT.FORWARD
   		threadL = threading.Thread(target=stepper_worker, args=(left, steps, left_dir, step_style))
		threadR = threading.Thread(target=stepper_worker, args=(right, steps, right_dir, step_style))
		threadL.start()
    	threadR.start()

    def turnLeft():
    	rotate(false, 200)

    def turnRight():
    	rotate(true, 200)


class RemoteSensing(object):


class Cell(object):
    def __init__(self):
        self.walls = {
            NORTH : False,
            WEST  : False, 
            EAST  : False,
            SOUTH : False
        }
        self.backPointer = ""; 
        self.visited = False;
        self.deadEnd = False; 


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	shield.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def stepper_worker(stepper, numsteps, direction, style):
	#print("Steppin!")
	stepper.step(numsteps, direction, style)
	#print("Done")

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
