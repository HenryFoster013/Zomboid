import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import os
import random
import Player as player
import Enemy as enemy

screen_width = 800
screen_height = 600
frame_counter = 0
zombie = enemy.Zombie(100,2,10,[60,60],10)
wave_num = 1
zombie_list = [zombie]
dead_zombie_list = []
multiplier = [1,3]
wave_timer = 600

zombie_count = len(zombie_list)
dead_zombie_count = len(dead_zombie_list)
total_zombie_count = 1

def Graphics(canvas):
    midpoint = [screen_width/2, screen_height/2]    
    offset = [midpoint[0] - player.player_position[0], midpoint[1] - player.player_position[1]]

    # BACKGROUND
    canvas.draw_image(background, (1920 / 2, 1080 / 2), (1920, 1080), (offset[0] + (1920 * 0.625), offset[1] + (1080 * 0.625)), (1920 * 1.25, 1080 * 1.25))

    # DEBUG

    #ZOMBIE DEATH SPRITE (TEMP)
    for zomb1 in dead_zombie_list:
        if zomb1.dead == True:
            frame = zomb1.DeathAnimation(zomb1.death_sprite,4)
            zombiepos = (offset[0] + zomb1.GetPosition()[0], offset[1] + zomb1.GetPosition()[1])
            canvas.draw_image(zomb1.death_sprite,((frame[0]) + 100, (frame[1]) + 100), (200, 200), zombiepos, (150,150), 0)

    # PLAYER ANIMATION
    canvas.draw_circle((midpoint[0], midpoint[1] + 30), 30, 1, 'rgba(0,0,0,0.5)', 'rgba(0,0,0,0.5)')
    rot = player.GetRotation()
    frame = player.GetAnimationFrame()
    shooting_add = 0;
    if(player.GetMuzzleFlash()):
        shooting_add = 600
    canvas.draw_image(player_spritesheet, ((200 * rot) + 100, (200 * frame) + 100 + shooting_add), (200, 200), midpoint, (150,150), 0)

    # ZOMBIE ANIMATION
    for zomb2 in zombie_list:
        if zomb2.dead == False:

            rot = zomb2.GetRotation()
            frame = zomb2.GetAnimationFrame()
            zombiepos = (offset[0] + zomb2.GetPosition()[0], offset[1] + zomb2.GetPosition()[1])
            if zomb2.GetSmooth():
                canvas.draw_circle((zombiepos[0], zombiepos[1] + 30), 30, 1, 'rgba(0,0,0,0.5)', 'rgba(0,0,0,0.5)')
            canvas.draw_image(zombie_spritesheet, ((200 * rot) + 100, (200 * frame) + 100), (200, 200), zombiepos, (150,150), 0)

    for projectile in player.current_projectiles:
        if(projectile.Alive()):
            for zombCollision in zombie_list:
                zombCollision.CheckCollisions(projectile.position)
            projectile.Update()
            offsettedPos = [projectile.position[0] + offset[0], projectile.position[1] + offset[1]]
            colour = "rgb(255,247,165)"
            canvas.draw_circle(offsettedPos, 3,1, colour, colour)

def Draw_Handler(canvas):
    global screen_width, screen_height, frame_counter
    frame_counter += 1
    player.Update()
    #zombie.Update()
    for zombieUpd in (zombie_list):
        zombieUpd.Update()
    wave_handler()
    Graphics(canvas)

def wave_handler():
    global zombie_count, zombie_list, wave_num, dead_zombie_list, multiplier,total_zombie_count, wave_timer
    for zombMove in zombie_list:
            if zombMove.dead == True:
                dead_zombie_list.append(zombMove)
                zombie_list.remove(zombMove)
                zombie_count = len(zombie_list)

    if zombie_count == 0:
        if wave_timer <= 0:
            print("wave cleared")
            wave_num += 1
            multiplier[0] = multiplier[0] * 2
            multiplier[1] = multiplier[1] * 2
            new_zombie_count = random.randint(multiplier[0],multiplier[1])
            while len(dead_zombie_list) != 0:
                for deadZomb in dead_zombie_list:
                    deadZomb.health = 100
                    deadZomb.position = spawn_location()
                    deadZomb.dead = False
                    deadZomb.speed = deadZomb.speed_buffer
                    zombie_list.append(deadZomb)
                    dead_zombie_list.remove(deadZomb)
                    zombie_count = len(zombie_list)
            for x in range(new_zombie_count):
                name = total_zombie_count 
                zombie_list.append(name)
                zombie_list[name] = enemy.Zombie(100,2,10,spawn_location(),10)
                total_zombie_count += 1


            wave_timer = 600
        else:
            wave_timer -= 1

def spawn_location():
    return [random.randint(100,800),random.randint(100,800)]

def mouse_handler(pos):
    print(pos)

def Key_Down_Handler(key):
    player.Handle_Input_Down(key)

def Key_Up_Handler(key):
    player.Handle_Input_Up(key)


walls = ["left_house_wall","middle_house_wall","right_house_wall"]
diagonal_walls = ["diagonal_house_wall"]

frame = simplegui.create_frame('Video Game', screen_width, screen_height)
frame.set_keydown_handler(Key_Down_Handler)
frame.set_keyup_handler(Key_Up_Handler)

frame.set_canvas_background('Black')
background = simplegui.load_image('https://drive.google.com/uc?id=1xsla4hN7u9LZ6UgyjJ088w_AHSubAd-f')
player_spritesheet = simplegui.load_image('https://drive.google.com/uc?id=1N4fyrxW-1Y7CLO-3va-EVbaZQ65CQHaJ')
zombie_spritesheet = simplegui.load_image('https://drive.google.com/uc?id=13FDMYzx1goduwwtE4WEganWopds8wMAo')


frame.set_draw_handler(Draw_Handler)
frame.set_mouseclick_handler(mouse_handler)
frame.start()