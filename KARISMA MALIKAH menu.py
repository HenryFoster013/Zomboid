import simplegui

WIDTH = 800
HEIGHT = 600

background_image_url = "https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/Title.png"
settings_background_url = "https://img.freepik.com/free-vector/digital-technology-engineering-digital-telecoms-concept-futuristic-technology-background-vector-illustration_587448-960.jpg?t=st=1742320160~exp=1742323760~hmac=f4261eefb16ff3971f3c0900c7f290e7460eed65529118a9f12f7bba45375130&w=1800"
music_url = "https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/music1.wav"

background_image = simplegui.load_image(background_image_url)
settings_background = simplegui.load_image(settings_background_url)
background_music = simplegui.load_sound(music_url)

SETTINGS_BUTTON_SIZE = 80
settings_button_pos = (20, HEIGHT - SETTINGS_BUTTON_SIZE - 20)
cog_image_url = "https://cdn-icons-png.flaticon.com/512/7835/7835443.png"
cog_image = simplegui.load_image(cog_image_url)

QUIT_BUTTON_WIDTH = 100
QUIT_BUTTON_HEIGHT = 50
quit_button_pos = (WIDTH - 120, HEIGHT - 60)

in_settings_menu = False

resolutions = {"16:9": (1280, 720), "4:3": (800, 600)}
current_resolution = (WIDTH, HEIGHT)

music_enabled = True
volume = 1.0
volume_bar_width = 150
volume_bar_height = 20
volume_slider_width = 10

volume_bar_pos = (WIDTH // 2 - 75, HEIGHT // 2 + 90)
volume_slider_pos = volume_bar_pos[0] + volume_bar_width - volume_slider_width

back_button_pos = (WIDTH // 2 - 60, HEIGHT - 100)
sfx_button_pos = (WIDTH // 2 - 75, HEIGHT - 150)

def toggle_music():
    global music_enabled
    if music_enabled: background_music.pause()
    else: background_music.play()
    music_enabled = not music_enabled

def open_settings():
    global in_settings_menu
    in_settings_menu = not in_settings_menu

def quit_game():
    frame.stop()

def set_resolution(aspect_ratio):
    global WIDTH, HEIGHT, current_resolution, frame
    global volume_bar_pos, volume_slider_pos, back_button_pos, sfx_button_pos
    WIDTH, HEIGHT = resolutions[aspect_ratio]
    current_resolution = (WIDTH, HEIGHT)
    volume_bar_pos = (WIDTH // 2 - 75, HEIGHT // 2 + 90)
    volume_slider_pos = volume_bar_pos[0] + volume_bar_width - volume_slider_width
    back_button_pos = (WIDTH // 2 - 60, HEIGHT - 100)
    sfx_button_pos = (WIDTH // 2 - 75, HEIGHT - 150)
    frame.stop()
    frame = simplegui.create_frame("ZombieTown", WIDTH, HEIGHT)
    frame.set_draw_handler(draw)
    frame.set_mouseclick_handler(click_handler)
    frame.start()

def update_volume(mouse_x):
    global volume, volume_slider_pos
    volume_slider_pos = max(volume_bar_pos[0], min(mouse_x, volume_bar_pos[0] + volume_bar_width - volume_slider_width))
    volume = (volume_slider_pos - volume_bar_pos[0]) / volume_bar_width
    background_music.set_volume(volume)

def click_handler(mouse_pos):
    x, y = mouse_pos
    if not in_settings_menu:
        settings_x, settings_y = settings_button_pos
        if settings_x <= x <= settings_x + SETTINGS_BUTTON_SIZE and settings_y <= y <= settings_y + SETTINGS_BUTTON_SIZE: open_settings()
        quit_x, quit_y = quit_button_pos
        if quit_x <= x <= quit_x + QUIT_BUTTON_WIDTH and quit_y <= y <= quit_y + QUIT_BUTTON_HEIGHT: quit_game()
    else:
        back_x, back_y = back_button_pos
        if back_x <= x <= back_x + 120 and back_y <= y <= back_y + 40: open_settings()
        sfx_x, sfx_y = sfx_button_pos
        if sfx_x <= x <= sfx_x + 150 and sfx_y <= y <= sfx_y + 40: toggle_music()
        button_x = WIDTH // 2 - 75
        button_width = 150
        button_height = 40
        if button_x <= x <= button_x + button_width and 260 <= y <= 260 + button_height: set_resolution("16:9")
        if button_x <= x <= button_x + button_width and 320 <= y <= 320 + button_height: set_resolution("4:3")
        volume_bar_x, volume_bar_y = volume_bar_pos
        if volume_bar_x <= x <= volume_bar_x + volume_bar_width and volume_bar_y <= y <= volume_bar_y + volume_bar_height: update_volume(x)

def draw(canvas):
    if not in_settings_menu:
        canvas.draw_image(background_image, (background_image.get_width() / 2, background_image.get_height() / 2), (background_image.get_width(), background_image.get_height()), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    else:
        canvas.draw_image(settings_background, (settings_background.get_width() / 2, settings_background.get_height() / 2), (settings_background.get_width(), settings_background.get_height()), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if not in_settings_menu:
        canvas.draw_image(cog_image, (cog_image.get_width() / 2, cog_image.get_height() / 2), (cog_image.get_width(), cog_image.get_height()), (settings_button_pos[0] + SETTINGS_BUTTON_SIZE / 2, settings_button_pos[1] + SETTINGS_BUTTON_SIZE / 2), (SETTINGS_BUTTON_SIZE, SETTINGS_BUTTON_SIZE))
        canvas.draw_polygon([(quit_button_pos[0], quit_button_pos[1]), (quit_button_pos[0] + QUIT_BUTTON_WIDTH, quit_button_pos[1]), (quit_button_pos[0] + QUIT_BUTTON_WIDTH, quit_button_pos[1] + QUIT_BUTTON_HEIGHT), (quit_button_pos[0], quit_button_pos[1] + QUIT_BUTTON_HEIGHT)], 1, "Black", "White")
        canvas.draw_text("Quit", (quit_button_pos[0] + 25, quit_button_pos[1] + 30), 20, "Black", "monospace")
    else:
        canvas.draw_text("Settings Menu", (WIDTH // 2 - 100, 140), 40, "White", "serif")
        canvas.draw_text("Select Aspect Ratio:", (WIDTH // 2 - 100, 190), 30, "Black")
        button_x = WIDTH // 2 - 75
        button_width = 150
        button_height = 40
        canvas.draw_polygon([(button_x, 260), (button_x + button_width, 260), (button_x + button_width, 260 + button_height), (button_x, 260 + button_height)], 1, "Black", "Gray")
        canvas.draw_text("16:9", (button_x + 50, 260 + 25), 20, "White")
        canvas.draw_polygon([(button_x, 320), (button_x + button_width, 320), (button_x + button_width, 320 + button_height), (button_x, 320 + button_height)], 1, "Black", "Gray")
        canvas.draw_text("4:3", (button_x + 50, 320 + 25), 20, "White")
        back_x, back_y = back_button_pos
        canvas.draw_polygon([(back_x, back_y), (back_x + 120, back_y), (back_x + 120, back_y + 40), (back_x, back_y + 40)], 1, "Black", "Black")
        canvas.draw_text("Back", (back_x + 35, back_y + 27), 20, "White", "serif")
        sfx_x, sfx_y = sfx_button_pos
        canvas.draw_polygon([(sfx_x, sfx_y), (sfx_x + 150, sfx_y), (sfx_x + 150, sfx_y + 40), (sfx_x, sfx_y + 40)], 1, "Black", "Gray" if music_enabled else "Red")
        canvas.draw_text("SFX: ON" if music_enabled else "SFX: OFF", (sfx_x + 30, sfx_y + 27), 20, "White")
        canvas.draw_text(f"Volume: {int(volume * 100)}%", (volume_bar_pos[0], volume_bar_pos[1] - 10), 20, "White")
        canvas.draw_polygon([(volume_bar_pos[0], volume_bar_pos[1]), (volume_bar_pos[0] + volume_bar_width, volume_bar_pos[1]), (volume_bar_pos[0] + volume_bar_width, volume_bar_pos[1] + volume_bar_height), (volume_bar_pos[0], volume_bar_pos[1] + volume_bar_height)], 1, "Black", "Gray")
        canvas.draw_polygon([(volume_slider_pos, volume_bar_pos[1]), (volume_slider_pos + volume_slider_width, volume_bar_pos[1]), (volume_slider_pos + volume_slider_width, volume_bar_pos[1] + volume_bar_height), (volume_slider_pos, volume_bar_pos[1] + volume_bar_height)], 1, "Black", "White")

frame = simplegui.create_frame("ZombieTown", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click_handler)
background_music.play()
background_music.set_volume(volume)
frame.start()