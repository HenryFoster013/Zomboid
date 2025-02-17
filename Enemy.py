import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import Projectiles as projectiles
import Player as player

class Zombie():
    def __init__(self,health, speed, damage, position):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.position = position
        self.cooldown = 0
        self.current_angle = 0;
        self.damage_cooldown = 0
        self.animation_frame = -1

    def FollowPlayer(self,player_position):
        self.x_difference = player_position[0] - self.position[0]
        self.y_difference = player_position[1] - self.position[1]

        displacement_magnitude = math.sqrt(self.x_difference**2 + self.y_difference**2)
        self.position[0] += (self.x_difference * self.speed)/displacement_magnitude
        self.position[1] += (self.y_difference * self.speed)/displacement_magnitude


    def CheckCollisions(self, position):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if (self.position[0] + 16.0 >= position[0] and self.position[0] - 16.0 <= position[0]) and self.position[1] + 16.0 >= position[1] and self.position[1] - 16.0 <= position[1]:
            if self.damage_cooldown == 0:
                self.health -= 25
                print("enemy hit")
                self.damage_cooldown = 50

    def check_death(self):
        if self.health <=0:
            print("enemy dead")
            self.position = [0,0]
            self.health = 100

    def Update(self):
        player_pos = [0,0]
        player_pos[0] = player.player_position[0]
        player_pos[1] = player.player_position[1]
        self.FollowPlayer(player_pos)
        self.check_death()

    def GetRotation(self)
        return self.current_angle

    def CalculateRotation(self, axis):
        match axis:
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
            animation_frame += 1
        else:
            animation_frame = -1

        if(animation_frame > 23):
            animation_frame = 0

        return animation_frame
