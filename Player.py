import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import Projectiles as projectiles
from Tile import *

player_position = [1152, 748]
movement_axis = [0,0]
shooting_axis = [0,0]
movement_speed = 8

shooting_cooldown = -1
max_cooldown = 6
projectile_lifetime = 180
max_projectiles = 20 # Total max needed without recycling any active bullets is projectile_lifetime // max_projectiles (30)
current_projectiles = []
current_pointer = -1
current_angle = 0
animation_frame = -1
movement_buffer = [-2,-2]

score = 0

#MOVEMENT VALUES
movement_up = False
movement_down = False
movement_left = False
movement_right = False

#COLLISION VALUES
up_collision = False
down_collision = False
left_collision = False
right_collision = False

for i in range(max_projectiles):
    current_projectiles.append(projectiles.bullet([0,0], [0,0], projectile_lifetime, False)) #CHANGE THIS

def fire_bullet():
    global shooting_cooldown, current_pointer, current_projectiles

    current_pointer += 1
    if(current_pointer >= max_projectiles):
        current_pointer = 0

    if(shooting_cooldown >= 0):
        newDir = [shooting_axis[0],shooting_axis[1]]
        offset = 45
        newPos = [player_position[0] + newDir[0] * offset,player_position[1] + newDir[1] * offset]
        current_projectiles[current_pointer].Startup(newPos, newDir, True)
        shooting_cooldown = -max_cooldown
        CalculateRotation(shooting_axis)

def Handle_Input_Down(key):
    global movement_up, movement_down, movement_left, movement_right
    match key:
        # WASD Movement
        case 87: #W
            movement_up = True
            movement_axis[1] += -1
            return
        case 83: #S
            movement_down = True
            movement_axis[1] += 1
            return
        case 65: #A
            movement_left = True
            movement_axis[0] += -1
            return
        case 68: #D
            movement_right = True
            movement_axis[0] += 1
            return

        # Arrow Key Shooting
        case 38: # Up Arrow
            shooting_axis[1] = -1
            fire_bullet()
            return
        case 40: # Down Arrow
            shooting_axis[1] = 1
            fire_bullet()
            return
        case 37: # Left Arrow
            shooting_axis[0] = -1
            fire_bullet()
            return
        case 39: # Right Arrow
            shooting_axis[0] = 1
            fire_bullet()
            return

def Handle_Input_Up(key):
    global movement_up,movement_down,movement_left,movement_right
    match key:
        # WASD Movement
        case 87: #W
            movement_up = False
            movement_axis[1] -= -1
            return
        case 83: #S
            movement_down = False
            movement_axis[1] -= 1
            return
        case 65: #A
            movement_left = False
            movement_axis[0] -= -1
            return
        case 68: #D
            movement_right = False
            movement_axis[0] -= 1
            return

        # Arrow Key Shooting
        case 38: # Up Arrow
            shooting_axis[1] = 0
            return
        case 40: # Down Arrow
            shooting_axis[1] = 0
            return
        case 37: # Left Arrow
            shooting_axis[0] = -0
            return
        case 39: # Right Arrow
            shooting_axis[0] = 0
            return
    
def Movement():
    global player_position, movement_axis, movement_speed, up_collision, down_collision, left_collision, right_collision
    # Normalise vector
    mod = 1
    if(movement_axis[0] != 0 and movement_axis[1] != 0):
        mod = 0.7071
    
    # Apply movement
    newx = player_position[0]
    newy = player_position[1]

    
    if movement_left and left_collision == False:
        newx = player_position[0] + (movement_axis[0] * movement_speed * mod)
    if movement_right and right_collision == False:
        newx = player_position[0] + (movement_axis[0] * movement_speed * mod)
    if movement_up and up_collision == False:
        newy = player_position[1] + (movement_axis[1] * movement_speed * mod)
    if movement_down and down_collision == False:
        newy = player_position[1] + (movement_axis[1] * movement_speed * mod)
    player_radius = 30
    if(newx < ((1920 * 1.25) - 60) and newx > 60):
        player_position[0] = newx
    if(newy < ((1080 * 1.25) - 80) and newy > 60):
        player_position[1] = newy

def GetRotation():
    return current_angle 

def GetAnimationFrame():
    global animation_frame
    if(movement_axis != [0,0]):
        animation_frame += 1
    else:
        animation_frame = -1

    frame_length = 6

    if(animation_frame > (frame_length * 4 - 1)):
        animation_frame = 0

    final_num = 0;
    if(animation_frame == -1 or (animation_frame >= frame_length and animation_frame < (frame_length * 2)) or (animation_frame >= (frame_length * 3))):
        final_num = 0;
    if(animation_frame >= (frame_length * 2) and animation_frame < (frame_length * 3)):
        final_num = 1
    if(animation_frame < frame_length and animation_frame > 0):
        final_num = 2

    return final_num

def GetMuzzleFlash():
    return (shooting_cooldown < 0)

def CalculateRotation(axis):
    global current_angle
    match axis:
        case [0,1]:
            current_angle = 4
            return
        case [1,1]:
            current_angle = 5
            return
        case [-1,1]:
            current_angle = 3
            return
        case [1,0]:
            current_angle = 6
            return
        case [-1,0]:
            current_angle = 2
            return
        case [1,-1]:
            current_angle = 7
            return
        case [-1,-1]:
            current_angle = 1
            return
        case [0,-1]:
            current_angle = 0
            return

def Shooting():
    global shooting_cooldown
    shooting_cooldown += 1

def Rotation():
    global movement_buffer
    if(movement_buffer[0] != movement_axis[0] or movement_buffer[1] != movement_axis[1]):
        if(shooting_axis == [0,0] and shooting_cooldown >= max_cooldown):
            CalculateRotation(movement_axis)
    movement_buffer[0] = movement_axis[0]
    movement_buffer[1] = movement_axis[1]

def wall_collision_check():
        global up_collision,down_collision,left_collision,right_collision
        up_collision = False
        down_collision = False
        left_collision = False
        right_collision = False
        for i in range(len(walls)):
            if walls[i].check_collision((player_position[0] + movement_speed), player_position[1]) == True:
                right_collision = True
                print("right collision")
            if walls[i].check_collision((player_position[0] - movement_speed), player_position[1]) == True:
                left_collision = True
                print("left collision")
            if walls[i].check_collision(player_position[0], (player_position[1] + movement_speed)) == True:
                down_collision = True
                print("down collision")
            if walls[i].check_collision(player_position[0], (player_position[1] - 10)) == True:
                up_collision = True
                print("up collision")

        for i in range(len(diagonal_walls)):
            if diagonal_walls[i].check_collision((player_position[0] + movement_speed), player_position[1]) == True:
                right_collision = True
            if diagonal_walls[i].check_collision((player_position[0] - movement_speed), player_position[1]) == True:
                left_collision = True
            if diagonal_walls[i].check_collision(player_position[0], (player_position[1] + movement_speed)) == True:
                down_collision = True
            if diagonal_walls[i].check_collision(player_position[0], (player_position[1] - movement_speed)) == True:
                up_collision = True

def Update():
    Movement()
    Shooting()
    Rotation()
    wall_collision_check()

