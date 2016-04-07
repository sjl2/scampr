#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper 
from Adafruit_MotorHAT import Adafruit_MotorHAT
from Adafruit_MotorHAT import Adafruit_DCMotor
from Adafruit_MotorHAT import Adafruit_StepperMotor

import threading
import time
import atexit
import Maze
import Cell

NORTH = 'N'
WEST = 'W'
EAST = 'E'
SOUTH = 'S'

#######################################################################
# MAIN
#######################################################################

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

scampr.stepForward(100)
scampr.turnLeft()
scampr.turnRight()

atexit.register(turnOffMotors)

#######################################################################

class Robot(object):
    row = 0
    col = 0

    def __init__(self, left_motor, right_motor, remote_sensing):
        self.maze = [[Cell() for x in range(16)] for x in range(16)] 
        self.current_direction = EAST

    def isSolved(self): 
        return (row == 7 or row == 8) and (col == 7 or col == 8)    

    def isVisited(self, direction):
        if direction is NORTH:
            return self.maze[row - 1][col].visited
        elif direction is WEST:
            return self.maze[row][col - 1].visited
        elif direction is EAST:
            return self.maze[row][col + 1].visited
        elif direction is SOUTH:
            return self.maze[row + 1][col].visited
        else:
            raise ValueError(direction 
                    + ' is not a valid direction (N, W, E, S).')
    
    def isWall(self, direction):
        return self.maze[row][col].walls[direction] 

    def isDeadEnd(self, direction):
        if direction is NORTH:
            return self.maze[row - 1][col].deadEnd
        elif direction is WEST:
            return self.maze[row][col - 1].deadEnd
        elif direction is EAST:
            return self.maze[row][col + 1].deadEnd
        elif direction is SOUTH:
            return self.maze[row + 1][col].deadEnd
        else:
            raise ValueError(direction
                    + ' is not a valid direction (N, W, E, S).')

    # Set the Back Pointer for the current cell to the cell in the 
    # direction direction. 
    def setBackPointer(self, direction):
        if direction is NORTH:
            self.maze[row][col].prevRow = row - 1
            self.maze[row][col].prevCol = col
        elif direction is WEST:
            self.maze[row][col].prevRow = row
            self.maze[row][col].prevCol = col - 1
        elif direction is EAST:
            self.maze[row][col].prevRow = row
            self.maze[row][col].prevCol = col + 1
        elif direction is SOUTH:
            self.maze[row][col].prevRow = row + 1
            self.maze[row][col].prevCol = col
        else:
            raise ValueError(direction 
                    + ' is not a valid direction (N, W, E, S).')
    
    def currIsDeadEnd(self):
        self.maze[row][col].deadEnd = True

    def currIsVisited(self):
        self.maze[row][col].visited = True


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
            NORTH : True,
            WEST  : True, 
            EAST  : True,
            SOUTH : True
        }
        self.prevRow = -1; 
        self.prevCol = -1; 
        self.visited = False
        self.deadEnd = False 


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	shield.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def getOppositeDirection(direction):
    if direction is NORTH:
        return SOUTH
    elif direction is WEST:
        return EAST
    elif direction is EAST:
        return WEST
    elif direction is SOUTH:
        return NORTH
    else:
        raise ValueError(direction 
                + ' is not a valid direction (N, W, E, S).')

def stepper_worker(stepper, numsteps, direction, style):
	#print("Steppin!")
	stepper.step(numsteps, direction, style)
	#print("Done")

