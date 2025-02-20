import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import Projectiles as projectiles
import Player as player
from Tile import *

class Zombie():
    def __init__(self,health, speed, damage, position):
        self.health = health
        self.speed = speed
        self.speed_buffer = speed
        self.damage = damage
        self.position = position
        self.cooldown = 0
        self.current_angle = 0;
        self.damage_cooldown = 0
        self.animation_frame = -1
        self.smooth = True
        
        self.up_collision = False
        self.down_collision = False
        self.left_collision = False
        self.right_collision = False

        self.dead = False

        self.death_animation_x = 0
        self.death_animation_y = 0
        self.death_animation_frame_count = -1
        self.death_animation_cooldown = 15

    def GetPosition(self):
        return self.position
    

    def DeathAnimation(self,death_sprite,frames):
        run = False
        set_frames = frames-2
        if self.health >= 0 and self.death_animation_frame_count < set_frames:
            run = True
        if run == True: 
            sprite = death_sprite
            if self.death_animation_cooldown <= 0:
                if self.death_animation_x >= 1600:
                        self.death_animation_x = 0
                        self.death_animation_y+= 200
                self.death_animation_x = self.death_animation_x + 200 
                self.death_animation_frame_count += 1
                self.death_animation_cooldown = 15
            else:
                self.death_animation_cooldown -=1
        return (self.death_animation_x, self.death_animation_y)
            


    def FollowPlayer(self, player_position):

        x_difference = player_position[0] - self.position[0]
        y_difference = player_position[1] - self.position[1]

        buffer = 40
        self.movement_axis = [0,0]
        if(x_difference > buffer) and self.right_collision == False:
            self.movement_axis[0] = 1
        elif(x_difference < -buffer) and self.left_collision == False:
            self.movement_axis[0] = -1
        else:
            self.movement_axis[0] = 0
        if(y_difference > buffer) and self.down_collision == False:
            self.movement_axis[1] = 1
        elif(y_difference < -buffer) and self.up_collision == False:
            self.movement_axis[1] = -1
        else:
            self.movement_axis[1] = 0

        if(self.smooth):
            self.SmoothFollowPlayer(player_position, x_difference, y_difference)
        else:
            self.FastFollowPlayer()

    def GetSmooth(self):
        return self.smooth
    
    def SmoothFollowPlayer(self, player_position, x_difference, y_difference):
        displacement_magnitude = math.sqrt(x_difference**2 + y_difference**2)
        if right_collision == False and x_difference > 0:
            self.position[0] += (x_difference * self.speed) / displacement_magnitude
        if left_collision == False and x_difference < 0:
            self.position[0] += (x_difference * self.speed) / displacement_magnitude
        if up_collision == False and y_difference < 0:
            self.position[1] += (y_difference * self.speed) / displacement_magnitude
        if down_collision == False and y_difference > 0:
            self.position[1] += (y_difference * self.speed) / displacement_magnitude

    def FastFollowPlayer(self):
        mod = 1
        if(self.movement_axis[0] != 0 and self.movement_axis[1] != 0):
            mod = 0.7071
        self.position = (self.position[0] + (self.movement_axis[0] * mod * self.speed), self.position[1] + (self.movement_axis[1] * mod * self.speed))

    def CheckCollisions(self, position):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if (self.position[0] + 23.0 >= position[0] and self.position[0] - 23.0 <= position[0]) and self.position[1] + 23.0 >= position[1] and self.position[1] - 23.0 <= position[1]:
            if self.damage_cooldown == 0:
                self.health -= 25
                print("enemy hit")
                self.damage_cooldown = 50

    def Death(self):
        if self.health <=0:
            #print("ZOMBO DEAD")
            self.speed = 0
            self.dead = True
            return self.dead


    def Update(self):
        self.wall_collision_check()
        self.FollowPlayer(player.player_position)
        self.Death()

    def GetRotation(self):
        self.CalculateRotation()
        return self.current_angle

    def CalculateRotation(self):
        match self.movement_axis:
            case [0,1]:
                self.current_angle = 4
                return
            case [1,1]:
                self.current_angle = 5
                return
            case [-1,1]:
                self.current_angle = 3
                return
            case [1,0]:
                self.current_angle = 6
                return
            case [-1,0]:
                self.current_angle = 2
                return
            case [1,-1]:
                self.current_angle = 7
                return
            case [-1,-1]:
                self.current_angle = 1
                return
            case [0,-1]:
                self.current_angle = 0
                return
    
    def GetAnimationFrame(self):
        if(self.movement_axis != [0,0]):
            self.animation_frame += 1
        else:
            self.animation_frame = -1

        frame_length = 6

        if(self.animation_frame > (frame_length * 4 - 1)):
            self.animation_frame = 0

        final_num = 0;
        if(self.animation_frame == -1 or (self.animation_frame >= frame_length and self.animation_frame < (frame_length * 2)) or (self.animation_frame >= (frame_length * 3))):
            final_num = 0;
        if(self.animation_frame >= (frame_length * 2) and self.animation_frame < (frame_length * 3)):
            final_num = 1
        if(self.animation_frame < frame_length and self.animation_frame > 0):
            final_num = 2

        return final_num
    
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
    
    death_sprite = simplegui.load_image("https://drive.google.com/uc?id=1R83lnLK6gZX9LlnsT8vv2wAFQsoiyple")
