import pygame as pg
import os

# Initialize pygame
pg.init()

# Set the script directory to ensure relative paths work correctly
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Screen setup
screen_width = 300
screen_height = 200
screen = pg.display.set_mode((screen_width, screen_height))

# Set icon and caption
icon_path ='../Images/Reload.png'
pg.display.set_icon(pg.image.load(icon_path))
pg.display.set_caption('Updater')

# Load font
font_path = '../Fonts/Rubik/static/Rubik-Regular.ttf'
font = pg.font.Font(font_path, 21)

# Clock setup
clock = pg.time.Clock()

# Update interval and text setup
update_interval = 150
last_update_time = 0
Times_dots_changed = 0
text_color = (225, 225, 225)
update_text = 'Updating application.'

running = True
while running:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill((30, 30, 30))  # Setting the fill color to dark gray

    # Update the text based on the interval
    current_time = pg.time.get_ticks()
    if current_time - last_update_time > update_interval:
        Times_dots_changed += 1
        if Times_dots_changed == 1:
            update_text = 'Updating application..'
        elif Times_dots_changed == 2:
            update_text = 'Updating application...'
        elif Times_dots_changed == 3:
            update_text = 'Updating application.'
            Times_dots_changed = 0
        last_update_time = current_time

    # Render the text
    text_surface = font.render(update_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 2)
    screen.blit(text_surface, text_rect)

    # Update the display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(248)

# Quit pygame
pg.quit()
