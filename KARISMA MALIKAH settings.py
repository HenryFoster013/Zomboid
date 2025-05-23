import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global Constants
WIDTH = 800
HEIGHT = 600

# Background Image and Music
background_image_url = "https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/Title.png"
music_url = "https://www.cs.rhul.ac.uk/home/znac189/ZOMBOID/music1.wav"
background_image = simplegui.load_image(background_image_url)
background_music = simplegui.load_sound(music_url)

# Cog Button Constants
SETTINGS_BUTTON_SIZE = 80
settings_button_pos = (20, HEIGHT - SETTINGS_BUTTON_SIZE - 20)
cog_image_url = "https://cdn-icons-png.flaticon.com/512/7835/7835443.png"
cog_image = simplegui.load_image(cog_image_url)

# Quit Button Constants
QUIT_BUTTON_WIDTH = 100
QUIT_BUTTON_HEIGHT = 50
quit_button_pos = (WIDTH - 120, HEIGHT - 60)

# Settings menu flags
in_settings_menu = False

# Resolution options
resolutions = {
    "16:9_720p": (1280, 720),
    "16:9_1080p": (1920, 1080),
    "16:9_1660p": (2560, 1660),
    "4:3_720p": (960, 720),
    "4:3_1080p": (1440, 1080),
    "4:3_1660p": (2213, 1660)
}
current_resolution = (WIDTH, HEIGHT)  # Default resolution

# Music toggle flag
music_enabled = True

# Brightness settings
brightness = 0  # 0 = fully bright, 255 = fully dark
brightness_bar_pos = (50, 400)  # Moved to the left side
brightness_bar_width = 150
brightness_bar_height = 20
brightness_slider_width = 10
brightness_slider_pos = brightness_bar_pos[0]  # Initial slider position

# Toggle Music Function
def toggle_music():
    global music_enabled
    if music_enabled:
        background_music.pause()  # Pause the music
    else:
        background_music.play()   # Play the music
    music_enabled = not music_enabled  # Toggle the flag

# Settings Menu Handler
def open_settings():
    global in_settings_menu
    in_settings_menu = not in_settings_menu
    if in_settings_menu:
        print("Settings menu opened.")
    else:
        print("Settings menu closed.")

def quit_game():
    print("Quit button pressed.")
    frame.stop()

# Set Resolution Function
def set_resolution(new_resolution):
    global current_resolution
    current_resolution = new_resolution
    print(f"Resolution changed to: {current_resolution[0]}x{current_resolution[1]}")

# Update Brightness Function
def update_brightness(mouse_x):
    global brightness, brightness_slider_pos
    # Ensure the slider stays within the brightness bar
    brightness_slider_pos = max(brightness_bar_pos[0], min(mouse_x - brightness_slider_width // 2, brightness_bar_pos[0] + brightness_bar_width - brightness_slider_width))
    # Calculate brightness value (0 to 255)
    brightness = int(((brightness_slider_pos - brightness_bar_pos[0]) / brightness_bar_width) * 255)

# Mouse Click Handler
def click_handler(mouse_pos):
    x, y = mouse_pos

    if not in_settings_menu:
        # Cog (Settings) Button
        settings_x, settings_y = settings_button_pos
        if settings_x <= x <= settings_x + SETTINGS_BUTTON_SIZE and settings_y <= y <= settings_y + SETTINGS_BUTTON_SIZE:
            open_settings()

        # Quit Button
        quit_x, quit_y = quit_button_pos
        if quit_x <= x <= quit_x + QUIT_BUTTON_WIDTH and quit_y <= y <= quit_y + QUIT_BUTTON_HEIGHT:
            quit_game()

    elif in_settings_menu:
        # Back Button
        back_x, back_y = WIDTH // 2 - 60, HEIGHT - 100
        if back_x <= x <= back_x + 120 and back_y <= y <= back_y + 40:
            open_settings()

        # Resolution Buttons
        button_x = WIDTH // 2 - 75
        button_width = 150
        button_height = 40

        # Check 16:9 Resolutions
        res_16_9 = [("16:9_720p", 260), ("16:9_1080p", 300), ("16:9_1660p", 340)]
        for res, y_pos in res_16_9:
            if button_x <= x <= button_x + button_width and y_pos <= y <= y_pos + button_height:
                set_resolution(resolutions[res])

        # Check 4:3 Resolutions
        res_4_3 = [("4:3_720p", 420), ("4:3_1080p", 460), ("4:3_1660p", 500)]
        for res, y_pos in res_4_3:
            if button_x <= x <= button_x + button_width and y_pos <= y <= y_pos + button_height:
                set_resolution(resolutions[res])

        # Music Toggle Switch
        music_toggle_x = WIDTH // 2 - 75
        music_toggle_y = 550
        if music_toggle_x <= x <= music_toggle_x + 150 and music_toggle_y <= y <= music_toggle_y + 40:
            toggle_music()

        # Brightness Bar
        brightness_bar_x, brightness_bar_y = brightness_bar_pos
        if brightness_bar_x <= x <= brightness_bar_x + brightness_bar_width and brightness_bar_y <= y <= brightness_bar_y + brightness_bar_height:
            update_brightness(x)

# Draw Handler
def draw(canvas):
    # Draw background image
    canvas.draw_image(background_image,
                      (background_image.get_width() / 2, background_image.get_height() / 2),
                      (background_image.get_width(), background_image.get_height()),
                      (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Apply brightness overlay
    canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)],
                        1, f"rgba(0, 0, 0, {brightness / 255})", f"rgba(0, 0, 0, {brightness / 255})")

    if not in_settings_menu:
        # Draw Cog (Settings) Button
        canvas.draw_image(cog_image,
                          (cog_image.get_width() / 2, cog_image.get_height() / 2),
                          (cog_image.get_width(), cog_image.get_height()),
                          (settings_button_pos[0] + SETTINGS_BUTTON_SIZE / 2, settings_button_pos[1] + SETTINGS_BUTTON_SIZE / 2),
                          (SETTINGS_BUTTON_SIZE, SETTINGS_BUTTON_SIZE))

        # Draw Quit Button
        canvas.draw_polygon([(quit_button_pos[0], quit_button_pos[1]),
                             (quit_button_pos[0] + QUIT_BUTTON_WIDTH, quit_button_pos[1]),
                             (quit_button_pos[0] + QUIT_BUTTON_WIDTH, quit_button_pos[1] + QUIT_BUTTON_HEIGHT),
                             (quit_button_pos[0], quit_button_pos[1] + QUIT_BUTTON_HEIGHT)],
                            1, "Black", "White")
        canvas.draw_text("Quit", (quit_button_pos[0] + 25, quit_button_pos[1] + 30), 20, "Black", "monospace")

    else:
        # SETTINGS MENU SCREEN
        canvas.draw_text("Settings Menu", (WIDTH // 2 - 100, 140), 40, "White", "serif")

        # Resolution Section
        canvas.draw_text("Select Resolution:", (WIDTH // 2 - 100, 190), 30, "Black")

        button_x = WIDTH // 2 - 75
        button_width = 150
        button_height = 40

        # Draw 16:9 Buttons
        canvas.draw_text("16:9 Aspect Ratio:", (WIDTH // 2 - 120, 250), 25, "Yellow")
        res_16_9 = [("16:9_720p", 260), ("16:9_1080p", 300), ("16:9_1660p", 340)]

        for res, y_pos in res_16_9:
            canvas.draw_polygon([(button_x, y_pos), (button_x + button_width, y_pos),
                                 (button_x + button_width, y_pos + button_height), (button_x, y_pos + button_height)],
                                1, "Black", "Gray")
            canvas.draw_text(res.split("_")[1], (button_x + 30, y_pos + 25), 20, "White")

        # Draw 4:3 Buttons
        canvas.draw_text("4:3 Aspect Ratio:", (WIDTH // 2 - 120, 400), 25, "Yellow")
        res_4_3 = [("4:3_720p", 420), ("4:3_1080p", 460), ("4:3_1660p", 500)]

        for res, y_pos in res_4_3:
            canvas.draw_polygon([(button_x, y_pos), (button_x + button_width, y_pos),
                                 (button_x + button_width, y_pos + button_height), (button_x, y_pos + button_height)],
                                1, "Black", "Gray")
            canvas.draw_text(res.split("_")[1], (button_x + 30, y_pos + 25), 20, "White")

        # Draw Back Button
        back_x = WIDTH // 2 - 60
        back_y = HEIGHT - 100
        canvas.draw_polygon([(back_x, back_y), (back_x + 120, back_y),
                             (back_x + 120, back_y + 40), (back_x, back_y + 40)],
                            1, "Black", "Black")
        canvas.draw_text("Back", (back_x + 35, back_y + 27), 20, "White", "serif")

        # Draw Music Toggle Switch
        music_toggle_x = WIDTH // 2 - 75
        music_toggle_y = 550
        canvas.draw_polygon([(music_toggle_x, music_toggle_y),
                            (music_toggle_x + 150, music_toggle_y),
                            (music_toggle_x + 150, music_toggle_y + 40),
                            (music_toggle_x, music_toggle_y + 40)],
                           1, "Black", "Gray" if music_enabled else "Red")
        canvas.draw_text("SFX: ON" if music_enabled else "SFX: OFF",
                         (music_toggle_x + 30, music_toggle_y + 27), 20, "White")

        # Draw Brightness Bar (on the left side)
        brightness_bar_x, brightness_bar_y = brightness_bar_pos
        canvas.draw_polygon([(brightness_bar_x, brightness_bar_y),
                            (brightness_bar_x + brightness_bar_width, brightness_bar_y),
                            (brightness_bar_x + brightness_bar_width, brightness_bar_y + brightness_bar_height),
                            (brightness_bar_x, brightness_bar_y + brightness_bar_height)],
                           1, "Black", "Gray")
        # Draw Brightness Slider
        canvas.draw_polygon([(brightness_slider_pos, brightness_bar_y),
                            (brightness_slider_pos + brightness_slider_width, brightness_bar_y),
                            (brightness_slider_pos + brightness_slider_width, brightness_bar_y + brightness_bar_height),
                            (brightness_slider_pos, brightness_bar_y + brightness_bar_height)],
                           1, "Black", "Blue")
        # Draw Brightness Label
        canvas.draw_text("Brightness", (brightness_bar_x, brightness_bar_y - 10), 20, "White", "serif")

# Create frame
frame = simplegui.create_frame("ZombieTown", WIDTH, HEIGHT)

# Register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click_handler)

# Start background music
background_music.play()

# Start the frame
frame.start() 
