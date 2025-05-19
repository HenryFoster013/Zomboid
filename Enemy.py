import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random
import Projectiles as projectiles
import Player as player
from Tile import *

class Zombie():
    def __init__(self,health, speed, damage, position, score_value, hit1, hit2, die1, die2):
        self.score_value = score_value
        self.health = health
        self.speed = random.randint(speed - 2, speed)
        self.speed_buffer = speed
        self.damage = damage
        self.position = position
        self.cooldown = 0
        self.current_angle = 0;
        self.damage_cooldown = 0
        self.animation_frame = -1
        self.movement_axis = [0,0]
        
        self.up_collision = False
        self.down_collision = False
        self.left_collision = False
        self.right_collision = False

        self.dead = False

        self.hit_1_sfx = hit1
        self.hit_2_sfx = hit2
        self.die_1_sfx = die1
        self.die_2_sfx = die2

        self.d_frame = 0

    def GetPosition(self):
        return self.position

    def DeathAnimation(self):
        
        frame_length = 16
        frame = 3

        if self.d_frame < frame_length:
            frame = 0
        elif self.d_frame >= frame_length and self.d_frame < frame_length * 2:
            frame = 1
        elif self.d_frame >= frame_length * 2 and self.d_frame < frame_length * 6:
            frame = 2
        
        self.d_frame += 1

        return frame        


    def FollowPlayer(self, player_position, player):

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

        self.SmoothFollowPlayer(player_position, x_difference, y_difference, player)
    
    def SmoothFollowPlayer(self, player_position, x_difference, y_difference, player):
        displacement_magnitude = math.sqrt(x_difference**2 + y_difference**2)

        if(displacement_magnitude < 24):
            player.TakeDamage()

        newX = self.position[0]
        newY = self.position[1]
        if self.right_collision == False and x_difference > 0:
            newX += (x_difference * self.speed) / displacement_magnitude
        if self.left_collision == False and x_difference < 0:
            newX += (x_difference * self.speed) / displacement_magnitude
        if self.up_collision == False and y_difference < 0:
            newY += (y_difference * self.speed) / displacement_magnitude
        if self.down_collision == False and y_difference > 0:
            newY += (y_difference * self.speed) / displacement_magnitude
        self.position = (newX, newY)

    def CheckCollisions(self, project):
        position = project.position
        killed = False
        if self.dead == False:
            self.damage_cooldown -= 1
            if (self.position[0] + 23.0 >= position[0] and self.position[0] - 23.0 <= position[0]) and self.position[1] + 23.0 >= position[1] and self.position[1] - 23.0 <= position[1]:
                if self.damage_cooldown < 0:
                    self.health -= 25
                    self.damage_cooldown = 3
                    sfx_switch = (random.randint(0,1) == 1)
                    if(self.health > 0):
                        if(sfx_switch):
                            self.hit_1_sfx.rewind()
                            self.hit_1_sfx.play()
                        else:
                            self.hit_2_sfx.rewind()
                            self.hit_2_sfx.play()
                    else:
                        killed = True
                        if(sfx_switch):
                            self.die_1_sfx.rewind()
                            self.die_1_sfx.play()
                        else:
                            self.die_2_sfx.rewind()
                            self.die_2_sfx.play()

                project.kill()

        return killed

    def Update(self):
        self.wall_collision_check()
        self.FollowPlayer(player.player_position, player)
        self.Death()
    
    def Death(self):
        if self.health <=0:
            self.speed = 0
            self.dead = True
            player.score += self.score_value
            return self.dead

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
        self.d_frame = 0
        if(self.movement_axis != [0,0]):
            self.animation_frame += 1
        else:
            self.animation_frame = -1

        frame_length = 8

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
        self.up_collision = False
        self.down_collision = False
        self.left_collision = False
        self.right_collision = False
        for i in range(len(walls)):
            if walls[i].check_collision((self.position[0] + self.speed), self.position[1]) == True:
                self.right_collision = True
            if walls[i].check_collision((self.position[0] - self.speed), self.position[1]) == True:
                self.left_collision = True
            if walls[i].check_collision(self.position[0], (self.position[1] + self.speed)) == True:
                self.down_collision = True
            if walls[i].check_collision(self.position[0], (self.position[1] - 10)) == True:
                self.up_collision = True

        for i in range(len(diagonal_walls)):
            if diagonal_walls[i].check_collision((self.position[0] + self.speed), self.position[1]) == True:
                self.right_collision = True
            if diagonal_walls[i].check_collision((self.position[0] - self.speed), self.position[1]) == True:
                self.left_collision = True
            if diagonal_walls[i].check_collision(self.position[0], (self.position[1] + self.speed)) == True:
                self.down_collision = True
            if diagonal_walls[i].check_collision(self.position[0], (self.position[1] - self.speed)) == True:
                self.up_collision = True