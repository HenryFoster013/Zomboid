import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
from Tile import *

class bullet:

    position = (0,0)
    direction = (0,0)
    mult = 1
    speed = 18
    lifetime = 180
    frame_counter = 0
    alive = False

    def __init__(self, _position, _direction, _lifetime, _alive):
        self.Startup(_position, _direction, _alive)

    def Startup(self, _position, _direction, _alive):
        self.position = _position
        self.direction = _direction
        self.alive = _alive
        if(self.direction[0] != 0 and self.direction[1] != 0):
            self.mult = 1 / math.sqrt(2)

    def Alive(self):
        return self.alive
    
    def Update(self):
        if(self.alive):
            self.wall_collision_check()
            self.position[0] += self.direction[0] * self.speed * self.mult
            self.position[1] += self.direction[1] * self.speed * self.mult
            self.frame_counter += 1
            #if(self.frame_counter >= self.lifetime):
            #    self.destroyThis()
    
    def wall_collision_check(self):
        global up_collision,down_collision,left_collision,right_collision
        up_collision = False
        down_collision = False
        left_collision = False
        right_collision = False
        for i in range(len(walls)):
            if walls[i].check_collision((self.position[0] + self.speed), self.position[1]) == True:
                right_collision = True
            if walls[i].check_collision((self.position[0] - self.speed), self.position[1]) == True:
                left_collision = True
            if walls[i].check_collision(self.position[0], (self.position[1] + self.speed)) == True:
                down_collision = True
            if walls[i].check_collision(self.position[0], (self.position[1] - 10)) == True:
                up_collision = True

        for i in range(len(diagonal_walls)):
            if diagonal_walls[i].check_collision((self.position[0] + self.speed), self.position[1]) == True:
                right_collision = True
            if diagonal_walls[i].check_collision((self.position[0] - self.speed), self.position[1]) == True:
                left_collision = True
            if diagonal_walls[i].check_collision(self.position[0], (self.position[1] + self.speed)) == True:
                down_collision = True
            if diagonal_walls[i].check_collision(self.position[0], (self.position[1] - self.speed)) == True:
                up_collision = True
