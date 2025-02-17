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
        self.target = []
        self.cooldown = 0
        self.movement_index = [0,0]
        self.damage_cooldown = 0
        zombie_angle = 0.0
        movement_axis = [0,0]
        animation_frame = -1
        zombie_spritesheet = simplegui.load_image('https://drive.google.com/file/d/12C-a-XqCjEXw_qxuIH9R6V8wKnJiMOrr/view?usp=sharing')

    def FollowPlayer(self,player_position):
        self.target = player_position
        x_difference = player_position[0] - self.position[0]
        y_difference = player_position[1] - self.position[1]
        displacement = [x_difference, y_difference]
        displacement_magnitude = math.sqrt(displacement[0]**2 + displacement[1]**2)
        self.position[0] += (displacement[0] * self.speed)/displacement_magnitude
        self.position[1] += (displacement[1] * self.speed)/displacement_magnitude


    def check_collision(self, position):
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

    def CalculateRotation():
        global zombie_angle, movement_axis
        match movement_axis:
            case [0,1]:
                zombie_angle = 3.14159265
                return
            case [1,1]:
                zombie_angle = 2.35619449
                return
            case [-1,1]:
                zombie_angle = 3.92699082
                return
            case [1,0]:
                zombie_angle = 1.57079633
                return
            case [-1,0]:
                zombie_angle = 4.71238898
                return
            case [1,-1]:
                zombie_angle = 0.78539816
                return
            case [-1,-1]:
                zombie_angle = 5.49778715
                return
            case [0,-1]:
                zombie_angle = 0
                return
    
    def GetRotation():
        return zombie_angle
    
    def GetAnimationFrame():
        global animation_frame
        if(movement_axis != [0,0]):
            animation_frame += 1
        else:
            animation_frame = -1

        if(animation_frame > 23):
            animation_frame = 0

        return animation_frame
