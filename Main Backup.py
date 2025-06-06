import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import os
import random
import Player as player
import Enemy as enemy
import Tile as tile

title_music = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/music1.wav')
game_music = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/music2.wav')
zomb_hit_1_sfx = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/Hit1.wav')
zomb_hit_2_sfx = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/Hit2.wav')
zomb_die_1_sfx = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/ZombieDie1.wav')
zomb_die_2_sfx = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/ZombieDie2.wav')
player_death_sfx = simplegui.load_sound('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/PlayerDeath.wav')

title_music.play()

fog = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/fog.png')
bgfog = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/bgfog.png')
background = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/FadedBG.png')
player_spritesheet = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/player.png')
player_hit = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/player_hurt.png')
zombie_spritesheet = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/zombie.png')
zombie_death_sprite = simplegui.load_image("https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/zombie_death.png")
game_over = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/GameOver.png')
title = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/Title.png')
blood = simplegui.load_image('https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/blood_with_fog.png')

screen_width = 800
screen_height = 600
frame_counter = 0
zombie = enemy.Zombie(100,6,10,[60,60],10, zomb_hit_1_sfx, zomb_hit_2_sfx, zomb_die_1_sfx, zomb_die_2_sfx)
wave_num = 1
zombie_list = [zombie]
dead_zombie_list = []
wave_timer = 600
bg_timer = 738
current_state = -1

current_score = 0
high_score = 0

f = open("highscore.txt", 'r')
high_score_text = f.read()
if(high_score_text == ""):
    high_score_text = "0"
high_score = int(high_score_text)

f.close()

zombie_count = len(zombie_list)
dead_zombie_count = len(dead_zombie_list)
total_zombie_count = 1

# UI Buttons
game_over_back_bounds = ((283, 517), (516,555))
start_bounds = ((37, 153), (180,190))
loading_game = False
loading_timer = 0

def Title_Screen(canvas):
    global loading_game, loading_timer, frame_counter, high_score
    canvas.draw_image(title, (400,300), (800,600), (screen_width / 2, screen_height / 2), (800, 600))
    trans_one = 1 - (frame_counter / 20)
    if(trans_one < 0):
        trans_one = 0
    canvas.draw_line((0, screen_height // 2), (screen_width, screen_height // 2), screen_width, 'rgba(0,0,0,' + str(trans_one) + ')')

    canvas.draw_text('HIGH SCORE: ' + str(high_score), (8, screen_height - 8), 30, 'Black', 'monospace')

    if loading_game:
        loading_timer += 1
        trans_two = (loading_timer / 60)
        if(trans_two > 1):
            trans_two = 1
            ResetGame()
        canvas.draw_line((0, screen_height // 2), (screen_width, screen_height // 2), screen_width, 'rgba(0,0,0,' + str(trans_two) + ')')

def Game_Over(canvas):
    canvas.draw_image(game_over, (400,300), (800,600), (screen_width / 2, screen_height / 2), (800, 600))
    transparency = 1 - (frame_counter / 30)
    if(transparency < 0):
        transparency = 0

    canvas.draw_text('FINAL SCORE: ' + str(current_score), ((screen_width // 2) - 90, (screen_height // 2) + 80), 20, 'rgb(225,10,55)', 'monospace')
    canvas.draw_line((0, screen_height // 2), (screen_width, screen_height // 2), screen_width, 'rgba(255,0,0,' + str(transparency) + ')')

def KillPlayer():
    global current_state, frame_counter, player_death_sfx, game, high_score, current_score
    current_state = 1
    frame_counter = 0
    player_death_sfx.rewind()
    game_music.pause()
    player_death_sfx.play()
    if(current_score > high_score):
        f = open("highscore.txt", "w")
        f.write(str(current_score))
        high_score = current_score
        f.close()


def Graphics(canvas):
    global current_score

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
                if(zombCollision.CheckCollisions(projectile)):
                    current_score += zombCollision.score_value

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
    canvas.draw_text('HP', (33, 48), 20, 'Black', 'monospace')
    canvas.draw_line((screen_width - 164, (HP_start[1])), (screen_width - 16, (HP_start[1])), HP_width + 6, 'Black')
    canvas.draw_text('WAVE: ' + str(wave_num), (screen_width - 160, 48), 20, 'White', 'monospace')
    canvas.draw_line((screen_width - 164, (HP_start[1] + 30)), (screen_width - 16, (HP_start[1] + 30)), HP_width + 6, 'Black')
    canvas.draw_text('SCORE: ' + str(current_score), (screen_width - 160, 78), 20, 'White', 'monospace')

    # FOG
    if(player.GetHealth() > 75): # GAME GETS LAGGY WITH SO MUCH TRANSPARENT OVERDRAW!! REMOVE FOG TO MAKE ROOM FOR BLOOD!!
        canvas.draw_image(fog, (1920 / 2, 1080 / 2), (1920, 1080), ((offset[0] * 1.5) + (1920 * 1.5) - 600, (offset[1] * 1.5) + (1080 * 1.5) - 400), (1920 * 3, 1080 * 3))

    # SCREEN BLOOD
    blood_level = (100 - player.GetHealth()) // 25
    if(blood_level == 1):
        canvas.draw_image(blood, (200, 150), (400, 300), (screen_width / 2, screen_height / 2), (screen_width, screen_height))
    elif(blood_level == 2):
        canvas.draw_image(blood, (200, 450), (400, 300), (screen_width / 2, screen_height / 2), (screen_width, screen_height))
    elif(blood_level > 2):
        canvas.draw_image(blood, (200, 750), (400, 300), (screen_width / 2, screen_height / 2), (screen_width, screen_height))

    # FADE IN
    transparency = 1 - (frame_counter / 30)
    if(transparency > 0):
        canvas.draw_line((0, screen_height // 2), (screen_width, screen_height // 2), screen_width, 'rgba(0,0,0,' + str(transparency) + ')')

def Draw_Handler(canvas):
    global screen_width, screen_height, frame_counter, bg_timer, current_state
    frame_counter += 1

    if(current_state == -1):
        Title_Screen(canvas)

    if(current_state == 0):
        player.Update()
        for zomb in (zombie_list):
            zomb.Update()
        wave_handler()
        
        if(player.GetHealth() <= 0):
            KillPlayer()
        else:
            Graphics(canvas)
    
    if(current_state == 1): # NOT AN ELSE IF!! Needs to override on the death frame!!
        Game_Over(canvas)

def wave_handler():
    global zombie_count, zombie_list, wave_num, dead_zombie_list, total_zombie_count, wave_timer, current_score
    for zombMove in zombie_list:
            if zombMove.dead == True:
                dead_zombie_list.append(zombMove)
                zombie_list.remove(zombMove)
                zombie_count = len(zombie_list)

    if zombie_count == 0:
        if wave_timer <= 0:
            print("wave cleared")
            current_score += 150
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
                zombie_list[name] = enemy.Zombie(100,6,10,spawn_location(),10, zomb_hit_1_sfx, zomb_hit_2_sfx, zomb_die_1_sfx, zomb_die_2_sfx)
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
    global current_state, loading_game
    if(current_state == 1):
        inX = position[0] < game_over_back_bounds[1][0] and position[0] > game_over_back_bounds[0][0]
        inY = position[1] < game_over_back_bounds[1][1] and position[1] > game_over_back_bounds[0][1]
        if (inX and inY):
            BackToMenu()
    
    if(current_state == -1):
        inX = position[0] < start_bounds[1][0] and position[0] > start_bounds[0][0]
        inY = position[1] < start_bounds[1][1] and position[1] > start_bounds[0][1]
        if (inX and inY):
            loading_game = True

def BackToMenu():
    global current_state, loading_game, loading_timer, frame_counter, player_death_sfx, title_music, game_music
    player_death_sfx.pause()
    game_music.pause()
    title_music.rewind()
    title_music.play()
    current_state = -1
    loading_game = False
    loading_timer = 0
    frame_counter = 0

def ResetGame():
    global wave_num, current_score, zombie_list, dead_zombie_list, wave_timer, bg_timer, current_state, zombie_count, dead_zombie_count, total_zombie_count, frame_counter, title_music, game_music
    current_score = 0
    title_music.pause()
    game_music.rewind()
    game_music.play()
    player.Reset()
    zombie = enemy.Zombie(100,6,10,spawn_location(),10, zomb_hit_1_sfx, zomb_hit_2_sfx, zomb_die_1_sfx, zomb_die_2_sfx)
    wave_num = 1
    zombie_list = [zombie]
    dead_zombie_list = []
    wave_timer = 600
    bg_timer = 738
    current_state = 0
    zombie_count = len(zombie_list)
    dead_zombie_count = len(dead_zombie_list)
    total_zombie_count = 1
    frame_counter = 0
    

frame = simplegui.create_frame('Video Game', screen_width, screen_height)
frame.set_keydown_handler(Key_Down_Handler)
frame.set_keyup_handler(Key_Up_Handler)
frame.set_mouseclick_handler(Mouse_Handler)

frame.set_canvas_background('Black')

frame.set_draw_handler(Draw_Handler)
frame.start()