#!/usr/bin/python

class Cell(object): 
    def __init__(self):		
        self.north_wall = True; 
        self.south_wall = True; 
        self.west_wall = True;
        self.east_wall = True; 
        self.back_ptr = ""; 
        self.visited = False; 
        self.dead_end = False; 

class Maze(object):
    def __init__(self):
        self.grid = [[Cell() for x in range(16)] for x in range(16)] 
