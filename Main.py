import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import os
import random
import Player as player
import Enemy as enemy
import Tile as tile

screen_width = 800
screen_height = 600
frame_counter = 0
zombie = enemy.Zombie(100,2,10,[60,60],10)
wave_num = 1
zombie_list = [zombie]
dead_zombie_list = []
wave_timer = 600
bg_timer = 738
current_state = 0

zombie_count = len(zombie_list)
dead_zombie_count = len(dead_zombie_list)
total_zombie_count = 1

game_over_back_bounds = ((361, 515), (454,556))

def Game_Over(canvas):
    canvas.draw_image(game_over, (400,300), (800,600), (screen_width / 2, screen_height / 2), (800, 600))
    transparency = 1 - (frame_counter / 30)
    if(transparency > 1):
        transparency = 1
    canvas.draw_line((0, screen_height // 2), (screen_width, screen_height // 2), screen_width, 'rgba(255,0,0,' + str(transparency) + ')')

def KillPlayer():
    global current_state, frame_counter
    current_state = 1
    frame_counter = 0

def Graphics(canvas):
    midpoint = [screen_width/2, screen_height/2]    
    offset = [midpoint[0] - player.player_position[0], midpoint[1] - player.player_position[1]]

    # BACKGROUND
    canvas.draw_image(bgfog, (400, 300), (800, 600), (screen_width / 2, screen_height / 2), (screen_width, screen_height))
    canvas.draw_image(background, (1920 / 2, 1080 / 2), (1920, 1080), (offset[0] + (1920 * 0.625), offset[1] + (1080 * 0.625)), (1920 * 1.25, 1080 * 1.25))

    # ZOMBIE DEATH SPRITE (TEMP)
    for zomb1 in dead_zombie_list:
        if zomb1.dead == True:
            frame = zomb1.DeathAnimation()
            zombiepos = (offset[0] + zomb1.GetPosition()[0], offset[1] + zomb1.GetPosition()[1])
            canvas.draw_image(zombie_death_sprite, ((frame * 200) + 100, 100), (200, 200), zombiepos, (162,162), 0)

    # PLAYER SHADOW
    canvas.draw_circle((midpoint[0], midpoint[1] + 30), 30, 1, 'rgba(0,0,0,0.5)', 'rgba(0,0,0,0.5)')

    # ZOMBIE ANIMATION
    smoothing = (len(zombie_list) < 10)
    for zomb in zombie_list:
        if zomb.dead == False:
            rot = zomb.GetRotation()
            frame = zomb.GetAnimationFrame()
            zombiepos = (offset[0] + zomb.GetPosition()[0], offset[1] + zomb.GetPosition()[1])
            if smoothing:
                canvas.draw_circle((zombiepos[0], zombiepos[1] + 30), 30, 1, 'rgba(0,0,0,0.5)', 'rgba(0,0,0,0.5)')
            canvas.draw_image(zombie_spritesheet, ((200 * rot) + 100, (200 * frame) + 100), (200, 200), zombiepos, (162,162), 0)

    # PLAYER ANIMATION
    rot = player.GetRotation()
    frame = player.GetAnimationFrame()
    shooting_add = 0
    if(player.GetMuzzleFlash()):
        shooting_add = 600
    sheet = player_spritesheet
    if(player.IsHurting()):
        sheet = player_hit
    canvas.draw_image(sheet, ((200 * rot) + 100, (200 * frame) + 100 + shooting_add), (200, 200), midpoint, (150,150), 0)

    for projectile in player.current_projectiles:
        if(projectile.Alive()):
            _alive = True
            for wall in tile.walls:
                if(wall.check_collision(projectile.position[0], projectile.position[1])):
                    _alive = False
            for wall in tile.diagonal_walls:
                if(wall.check_collision(projectile.position[0], projectile.position[1])):
                    _alive = False
            if(not _alive):
                projectile.kill()
            
            for zombCollision in zombie_list:
                zombCollision.CheckCollisions(projectile)
            projectile.Update()
            offsettedPos = [projectile.position[0] + offset[0], projectile.position[1] + offset[1]]
            colour = "rgb(255,247,165)"
            canvas.draw_circle(offsettedPos, 3,1, colour, colour)

    # UI
    HP_offset = (30,30)
    HP_width = 20
    HP_length = 1.5 * player.GetHealth()
    HP_start = (HP_offset[0], HP_offset[1] + (HP_width // 2))
    HP_end = (HP_offset[0] + HP_length, HP_offset[1] + (HP_width // 2))
    canvas.draw_line((HP_start[0] - 3, HP_start[1]), (HP_offset[0] + 153, HP_end[1]), HP_width + 6, 'Black')
    canvas.draw_line(HP_start, HP_end, HP_width, 'Red')
    canvas.draw_text('HP', (33, 48), 20, 'Black')
    canvas.draw_line((screen_width - 124, (HP_start[1])), (screen_width - 16, (HP_start[1])), HP_width + 6, 'Black')
    canvas.draw_text('WAVE: ' + str(wave_num), (screen_width - 120, 48), 20, 'White')

    # FOG
    canvas.draw_image(fog, (1920 / 2, 1080 / 2), (1920, 1080), ((offset[0] * 1.5) + (1920 * 1.5) - 600, (offset[1] * 1.5) + (1080 * 1.5) - 400), (1920 * 3, 1080 * 3))

def Draw_Handler(canvas):
    global screen_width, screen_height, frame_counter, bg_timer, current_state
    frame_counter += 1

    if(current_state == 0):
        player.Update()
        for zomb in (zombie_list):
            zomb.Update()
        wave_handler()
        
        bg_timer -= 1
        if(bg_timer <= 0):
            bg_timer = 738
            bgmusic.play()
        if(player.GetHealth() <= 0):
            KillPlayer()
        else:
            Graphics(canvas)
    
    if(current_state == 1): # NOT AN ELSE IF!! Needs to override on the death frame!!
        Game_Over(canvas)

def wave_handler():
    global zombie_count, zombie_list, wave_num, dead_zombie_list, total_zombie_count, wave_timer
    for zombMove in zombie_list:
            if zombMove.dead == True:
                dead_zombie_list.append(zombMove)
                zombie_list.remove(zombMove)
                zombie_count = len(zombie_list)

    if zombie_count == 0:
        if wave_timer <= 0:
            print("wave cleared")
            wave_num += 1
            new_zombie_count = 3
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


            wave_timer = 300
        else:
            wave_timer -= 1

def spawn_location():
    vert_horizontal = (random.randint(0,1) == 1)
    left_right = (random.randint(0,1) == 1)
    xpos = 0
    ypos = 0

    if(vert_horizontal):
        if(left_right):
            ypos = 1550
        else:
            ypos = -200
        xpos = random.randint(-200, 2600)
    else:
        if(left_right):
            xpos = 2600
        else:
            xpos = -200
        ypos = random.randint(-200, 1550)

    return [xpos,ypos]

def Key_Down_Handler(key):
    player.Handle_Input_Down(key)

def Key_Up_Handler(key):
    player.Handle_Input_Up(key)


def Mouse_Handler(position):
    global current_state
    if(current_state == 1):
        inX = position[0] < game_over_back_bounds[1][0] and position[0] > game_over_back_bounds[0][0]
        inY = position[1] < game_over_back_bounds[1][1] and position[1] > game_over_back_bounds[0][1]
        if (inX and inY):
            BackToMenu()

def BackToMenu():
    ResetGame()

def ResetGame():
    global wave_num, zombie_list, dead_zombie_list, wave_timer, bg_timer, current_state, zombie_count, dead_zombie_count, total_zombie_count
    player.Reset()
    zombie = enemy.Zombie(100,2,10,[60,60],10)
    wave_num = 1
    zombie_list = [zombie]
    dead_zombie_list = []
    wave_timer = 600
    bg_timer = 738
    current_state = 0
    zombie_count = len(zombie_list)
    dead_zombie_count = len(dead_zombie_list)
    total_zombie_count = 1
    

frame = simplegui.create_frame('Video Game', screen_width, screen_height)
frame.set_keydown_handler(Key_Down_Handler)
frame.set_keyup_handler(Key_Up_Handler)
frame.set_mouseclick_handler(Mouse_Handler)

frame.set_canvas_background('Black')

bgmusic = simplegui.load_sound('https://drive.google.com/uc?id=1KYtHghOEherZE_Lp9ZhZghRWVI8nmqmp')
bgmusic.play()
#zombie_death = simplegui.load_sound('https://drive.google.com/uc?id=113RkSNdnkkzjqzHPKdryopckHHCrHu-O')
#zombie_hit = simplegui.load_sound('https://drive.google.com/uc?id=1TvVuUmrZ96RQ3jWNZ4X8DA9ZRBbab5Zr')

fog = simplegui.load_image('https://drive.google.com/uc?id=13mg7pLi-NKC_CotzXw2ekIOKnjyuJ8hf')
bgfog = simplegui.load_image('https://drive.google.com/uc?id=1KScILrlQKk9tMGTPWE6V5udo6HIRrxjC')
background = simplegui.load_image('https://drive.google.com/uc?id=1xsla4hN7u9LZ6UgyjJ088w_AHSubAd-f')
player_spritesheet = simplegui.load_image('https://drive.google.com/uc?id=1N4fyrxW-1Y7CLO-3va-EVbaZQ65CQHaJ')
player_hit = simplegui.load_image('https://drive.google.com/uc?id=1qoXoueTpBJM_aH_7e0nO_2n_RbeeQ6Pz')
zombie_spritesheet = simplegui.load_image('https://drive.google.com/uc?id=13FDMYzx1goduwwtE4WEganWopds8wMAo')
zombie_death_sprite = simplegui.load_image("https://drive.google.com/uc?id=1C1UpxSsLsHZQIaBPimZ8RmpJD3tHYwtN")
game_over = simplegui.load_image('https://drive.google.com/uc?id=1ajbf2c1VxG3k-G_M6DxRad_QZSvCk2eK')


frame.set_draw_handler(Draw_Handler)
frame.start()