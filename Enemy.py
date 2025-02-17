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
        self.smooth = True

    def GetPosition(self):
        return self.position

    def FollowPlayer(self, player_position):
        x_difference = player_position[0] - self.position[0]
        y_difference = player_position[1] - self.position[1]

        buffer = 40
        self.movement_axis = [0,0]
        if(x_difference > buffer):
            self.movement_axis[0] = 1
        elif(x_difference < -buffer):
            self.movement_axis[0] = -1
        if(y_difference > buffer):
            self.movement_axis[1] = 1
        elif(y_difference < -buffer):
            self.movement_axis[1] = -1

        if(self.smooth):
            self.SmoothFollowPlayer(player_position, x_difference, y_difference)
        else:
            self.FastFollowPlayer()

    def GetSmooth(self):
        return self.smooth
    
    def SmoothFollowPlayer(self, player_position, x_difference, y_difference):
        displacement_magnitude = math.sqrt(x_difference**2 + y_difference**2)
        self.position[0] += (x_difference * self.speed) / displacement_magnitude
        self.position[1] += (y_difference * self.speed) / displacement_magnitude

    def FastFollowPlayer(self):
        mod = 1
        if(movement_axis[0] != 0 and movement_axis[1] != 0):
            mod = 0.7071
        self.position = (self.position[0] + (movement_axis[0] * mod * self.speed), self.position[1] + (movement_axis[1] * mod * self.speed))

    def CheckCollisions(self, position):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if (self.position[0] + 16.0 >= position[0] and self.position[0] - 16.0 <= position[0]) and self.position[1] + 16.0 >= position[1] and self.position[1] - 16.0 <= position[1]:
            if self.damage_cooldown == 0:
                self.health -= 25
                print("enemy hit")
                self.damage_cooldown = 50

    def Death(self):
        if self.health <=0:
            print("ZOMBO DEAD")

    def Update(self):
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
