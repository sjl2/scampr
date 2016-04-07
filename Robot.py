#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper 
from Adafruit_MotorHAT import Adafruit_MotorHAT
from Adafruit_MotorHAT import Adafruit_DCMotor
from Adafruit_MotorHAT import Adafruit_StepperMotor

import threading
import time
import atexit


# Constants
NORTH = 'N'
WEST = 'W'
EAST = 'E'
SOUTH = 'S'
DIRECTIONS = [NORTH, WEST, EAST, SOUTH]

RPM = 50
NINETY_DEGREES = 200 # STEPS
CELL_LENGTH = 400 # STEPS

# Global Initialization

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	shield.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	shield.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

# create a default object, no changes to I2C address or frequency
shield = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
threadL = threading.Thread()
threadR = threading.Thread()
threadL.daemon = True
threadR.daemon = True

# Motor Initialization
left = shield.getStepper(200, 1)  	# 200 steps/rev, motor port #1
right = shield.getStepper(200, 2)

left.setSpeed(RPM)  			# 30 RPM
right.setSpeed(RPM)  		        # 30 RPM
step_style = Adafruit_MotorHAT.SINGLE   #INTERLEAVE

class RemoteSensing(object):
    def __init__(self):
        pass


# Remote Sensining Initialization
remote_sensing = RemoteSensing()


class Cell(object):
    def __init__(self):
        self.walls = {
            NORTH : True,
            WEST  : True, 
            EAST  : True,
            SOUTH : True
        }
        self.BP = ""
        self.visited = False
        self.EV = False 


def oppositeDirection(direction):
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


class Robot(object):
    row = 0
    col = 0
    facing = EAST
    
    def __init__(self):
        self.maze = [[Cell() for x in range(16)] for x in range(16)] 

    def isSolved(self): 
        return (row == 7 or row == 8) and (col == 7 or col == 8)    
    
    def isCurrentVisited(self, direction):
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

    def isEV(self, direction):
        if direction is NORTH:
            return self.maze[row - 1][col].EV
        elif direction is WEST:
            return self.maze[row][col - 1].EV
        elif direction is EAST:
            return self.maze[row][col + 1].EV
        elif direction is SOUTH:
            return self.maze[row + 1][col].EV
        else:
            raise ValueError(direction
                    + ' is not a valid direction (N, W, E, S).')

    def getCurrentBP(self):
        return self.maze[row][col].BP

    # Direction should point to the previous room
    def setCurrentBP(self, direction):
        self.maze[row][col].BP = direction 

    def setEV(self):
        self.maze[row][col].EV = True

    def setVisited(self):
        self.maze[row][col].visited = True


    def stepForward(self, steps):
        global threadL
        global threadR

        print('Stepping Forward')
        threadL = threading.Thread(target=stepper_worker, args=(left, steps, Adafruit_MotorHAT.FORWARD, step_style))
	threadR = threading.Thread(target=stepper_worker, args=(right, steps, Adafruit_MotorHAT.FORWARD, step_style))
        
        threadL.daemon = True
        threadR.daemon = True

	threadL.start()
    	threadR.start()

        threadL.join()
        threadR.join()

    def stepForwardCarefully(self):
        # TODO Move with correction
        stepForward(CELL_LENGTH) 

    def rotate(self, cw, steps):
        global threadL
        global threadR

        print('Rotating')
        left_dir = Adafruit_MotorHAT.FORWARD
        right_dir = Adafruit_MotorHAT.BACKWARD
        
        if not cw:
            left_dir = Adafruit_MotorHAT.BACKWARD
            right_dir = Adafruit_MotorHAT.FORWARD
        
        threadL = threading.Thread(target=stepper_worker, args=(left, steps, left_dir, step_style))
        threadR = threading.Thread(target=stepper_worker, args=(right, steps, right_dir, step_style))

        threadL.daemon = True
        threadR.daemon = True
        
        threadL.start()
        threadR.start()

        threadL.join()
        threadR.join()

    def turnLeft(self):
        print('Turning Left')
    	self.rotate(False, NINETY_DEGREES)

    def turnRight(self):
        print('Turning Right')
    	self.rotate(True, NINETY_DEGREES)
        
    def turnAround(self):
        print('Turning Around')
        self.rotate(True, 2 * NINETY_DEGREES)

    def face(self, direction):
        if direction is NORTH:
            if facing is NORTH:
                pass
            elif facing is WEST:
                self.turnRight()
            elif facing is EAST:
                self.turnLeft()
            elif facing is SOUTH:
                self.turnAround()
            else:
                raise ValueError(direction 
                    + ' is not a valid direction (N, W, E, S).')
        elif direction is WEST:
            if facing is NORTH:
                self.turnLeft()
            elif facing is WEST:
                pass
            elif facing is EAST:
                self.turnAround()
            elif facing is SOUTH:
                self.turnRight()
            else:
                raise ValueError(direction 
                    + ' is not a valid direction (N, W, E, S).')
        elif direction is EAST:
            if facing is NORTH:
                self.turnRight()
            elif facing is WEST:
                self.turnAround()
            elif facing is EAST:
                pass
            elif facing is SOUTH:
                self.turnLeft()
            else:
                raise ValueError(direction 
                    + ' is not a valid direction (N, W, E, S).')
        elif direction is SOUTH:
            if facing is NORTH:
                self.turnAround()
            elif facing is WEST:
                self.turnLeft()
            elif facing is EAST:
                self.turnRight()
            elif facing is SOUTH:
                pass
            else:
                raise ValueError(direction 
                    + ' is not a valid direction (N, W, E, S).')
        else:
            raise ValueError(direction 
                + ' is not a valid direction (N, W, E, S).')

    def move(self, direction):
        self.face(direction)
        self.stepForwardCarefully()
        if direction is NORTH:
            row -= 1
        elif direction is WEST:
            col -= 1
        elif direction is EAST:
            col += 1
        elif direction is SOUTH:
            row += 1
        else:
            raise ValueError(direction 
                + ' is not a valid direction (N, W, E, S).')

    def wipeAllVisited(self):
        for row in self.maze:
            for c in row:
                c.visited = False

    def solveMaze(self):
        # Initial Solve
        keepExploring = False
        while not self.isSolved():
            keepExploring = False
            if not self.isCurrentVisited():
                self.updateWalls()
                self.currVisited()
            
            for dir in DIRECTIONS:
                if not (self.isWall(dir) or dir is self.getBP() or isEV(dir) or isVisited(dir)):
                    move(dir)
                    setBP(oppositeDirection(dir))
                    keepExploring = True
                    break
                
            if not keepExploring:
                self.setEV()
                self.move(self.BP())

        # First Solve Done
        bestPath = Queue.LifoQueue()
        prevBP = self.getBP()
        self.move(prevBP)
        while row is not 0 and col is not 0:
            currBP = getBP()
            bestPath.put(oppositeDirection(prevBP))
            #self.setBP(oppositeDirection(prevBP))
            
            for dir in DIRECTIONS:
                # TODO Why did you check if the room you're pointing at points back?
                if not (self.isWall(dir) or dir is oppositeDirection(prevBP) or self.isEV(dir)) and self.isVisited(dir):
                    currBP = dir
                    break

            move(currBP)
            prevBP = currBP
        
        bestPath.put(oppositeDirection(prevBP))
        #self.setBP(oppositeDirection(prevBP))

        while not bestPath.empty():
            move(bestPath.get())
            #move(self.getBP())

        self.wipeAllVisited()



#######################################################################
# MAIN
#######################################################################

# Robot Initialization
scampr = Robot()

scampr.stepForward(200)
#scampr.turnLeft()
#scampr.turnRight()

#######################################################################
