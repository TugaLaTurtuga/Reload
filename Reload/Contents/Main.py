import os
import json
import pygame as pg

pg.init()
pg.mixer.init()

import ForderFinder, Menus, SliderCode, Main_menu

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

screen_width = 800
screen_height = 600
visible = True
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(pg.image.load('Images/Reload.png'))
pg.display.set_caption('Reload')

LeftRectwidth = screen_width // 10
size = LeftRectwidth // 1.75
btns = []
btns_pos = []
btns_do = []


# Clock for controlling FPS
clock = pg.time.Clock()

def toggle_visibility():
    global visible, screen
    if visible:
        os.environ['SDL_VIDEODRIVER'] = ''  # Set to default to make the window visible
        screen = pg.display.set_mode((screen_width, screen_height), pg.NOFRAME)
    else:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Set to dummy to make the window invisible
        screen = pg.display.set_mode((1, 1), pg.NOFRAME)
    visible = not visible


# Function to make an icon round
def make_icon(icon):
    global size
    top_left_color = icon.get_at((5, 5))

    count_under_50 = sum(1 for value in top_left_color if value < 50)
    if count_under_50 >= 2:
        border_color = (
            min(255, int(top_left_color[0] * 1.2)),
            min(255, int(top_left_color[1] * 1.2)),
            min(255, int(top_left_color[2] * 1.2))
        )
    else:
        border_color = (
            max(0, top_left_color[0] // 2),
            max(0, top_left_color[1] // 2),
            max(0, top_left_color[2] // 2)
        )

    icon = pg.transform.scale(icon, (size, size))
    mask = pg.Surface((size, size), pg.SRCALPHA)
    pg.draw.rect(mask, (255, 255, 255), (0, 0, size, size), border_radius=2)
    icon.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)

    return icon

# Function to display folder icons
json_file_path = 'Saves/Favotites.json'
post_favourite = []
def display_folders(albums, singles, dt):
    y_plus_offset = 10
    y_offset = y_plus_offset * 2.5 - Main_menu.music_slider.value

    global btns, btns_pos, btns_do, json_file_path, screen, LeftRectwidth, size, post_favourite

    # Reset btns, btns_pos, btns_do
    btns = []
    btns_pos = []
    btns_do = []

    # Reload icon
    reload_icon_path = 'Images/Reload.png'
    try:
        reload_icon = make_icon(pg.image.load(reload_icon_path))
        screen.blit(reload_icon, (LeftRectwidth / 2 - size / 2, y_offset))
    except FileNotFoundError:
        print(f"Error: Reload icon not found at {reload_icon_path}")
        return

    btns.append(len(btns))
    btns_pos.append((LeftRectwidth / 2 - size / 2, y_offset))
    btns_do.append(lambda: Menus.change_Play_album())

    y_offset += reload_icon.get_height() + y_plus_offset
    try:
        # Read the existing JSON file
        with open(json_file_path, 'r') as f:
            favourites = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty list
        favourites = []
    except json.JSONDecodeError:
        # If the file contains invalid JSON, create an empty list
        favourites = []

    # Ensure favourites is a list
    if isinstance(favourites, str):
        favourites = [favourites]



    if favourites != []:
        for favourite in favourites:
            if os.path.exists(favourite):
                album_path = os.path.dirname(favourite)
                icon_path = os.path.join(album_path, 'icon.png')
                if not os.path.exists(icon_path):
                    icon_path = 'Images/Volume/full_volume.png'
                try:
                    icon = make_icon(pg.image.load(icon_path))
                    screen.blit(icon, (LeftRectwidth / 2 - size / 2, y_offset))
                    path_components = album_path.split('/')
                    album_index = len(btns)  # Capture the current index
                    btns.append(album_index)
                    btns_pos.append((LeftRectwidth / 2 - size / 2, y_offset))
                    btns_do.append(
                        lambda fav=favourite, path=album_path, comp=path_components[2]: ForderFinder.play_music(fav, comp, path,True))
                except Exception as e:
                    print(f"Error loading icon for {album_path}: {e}")
                y_offset += reload_icon.get_height() + y_plus_offset
            else:
                favourites.remove(favourite)
                with open(json_file_path, 'w') as f:
                    json.dump(favourites, f, indent=4)
    else:
        albums, singles = ForderFinder.search_folders()
        for album in albums:
            icon_path = os.path.join('Music/Album', album, 'icon.png')
            if not os.path.exists(icon_path):
                icon_path = 'Images/Volume/full_volume.png'
            icon = make_icon(pg.image.load(icon_path))
            screen.blit(icon, (LeftRectwidth / 2 - size / 2, y_offset))

            btns.append(len(btns))
            btns_pos.append((LeftRectwidth / 2 - size / 2, y_offset))
            btns_do.append(
                lambda music=album: ForderFinder.play_music(os.path.join('Music/Album', music, 'Album.mp3'), music,
                                                            os.path.join('Music/Album', music), True))

            y_offset += reload_icon.get_height() + y_plus_offset

        for single in singles:
            icon_path = os.path.join('Music/Single', single, 'icon.png')
            if not os.path.exists(icon_path):
                icon_path = 'Images/Volume/full_volume.png'
            icon = make_icon(pg.image.load(icon_path))
            screen.blit(icon, (LeftRectwidth / 2 - size / 2, y_offset))

            btns.append(len(btns))
            btns_pos.append((LeftRectwidth / 2 - size / 2, y_offset))
            btns_do.append(
                lambda music=single: ForderFinder.play_music(os.path.join('Music/Single', music, 'Single.mp3'),
                                                             music, os.path.join('Music/Single', music), True))
            y_offset += reload_icon.get_height() + y_plus_offset

    if y_offset > screen_height:
        Main_menu.__music_slider__(y_offset - size - y_plus_offset * 2)
        Main_menu.music_slider.update(dt / 1000)
        Main_menu.music_slider.draw(screen)

        if post_favourite != favourites:
            Main_menu.update_music_slider = True
            post_favourite = favourites


albums, singles = ForderFinder.get_folders()
# Game loop
already_pressed = False
running = True
toggle_visibility()
while running:
    # Limit frames per second
    dt = clock.tick(512)
    screen.fill((10, 10, 10))  # Fill the screen with a dark color

    # Get mouse input and/or change cursor
    mouse = pg.mouse.get_pos()
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_b or event.key == pg.K_UP:
                toggle_visibility()
            elif event.key == pg.K_n or event.key == pg.K_RIGHT:
                Menus.skip_music()
            elif event.key == pg.K_v or event.key == pg.K_LEFT:
                Menus.past_music()
            elif event.key == pg.K_SPACE:
                ForderFinder.un_pause_music()
            elif event.key == pg.K_m or event.key == pg.K_DOWN:
                Menus.change_Play_album()
        elif event.type == pg.MOUSEBUTTONDOWN and not already_pressed and event.button == 1:
            for i, btn in enumerate(btns):
                if btns_pos[i][0] <= mouse[0] <= btns_pos[i][0] + size and btns_pos[i][1] <= mouse[1] <= btns_pos[i][1] + size:
                    btns_do[i]()
                    break
            already_pressed = True
            Menus.__On_click__(mouse, event)
        elif event.type == pg.MOUSEBUTTONUP:
            already_pressed = False
        Menus.__SLiders_event__(event, mouse)
        Main_menu.music_slider.handle_event(event, mouse)

    Menus.__Menu__(screen, screen_width, screen_height, LeftRectwidth, dt)
    Menus.__Sliders__(screen)

    rect = pg.Rect(0, 0, LeftRectwidth, screen_height)  # Top-left corner
    pg.draw.rect(screen, (10, 10, 10), rect, border_radius=10)

    display_folders(albums, singles, dt)

    #Change cursor
    cursor_set = False
    for i, btn in enumerate(btns):
        if btns_pos[i][0] <= mouse[0] <= btns_pos[i][0] + size and btns_pos[i][1] <= mouse[1] <= btns_pos[i][1] + size:
            cursor_set = True
            break
    Menus.__On_hover__(mouse)

    if cursor_set or Menus.set_cursor or SliderCode.set_cursor:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
    else:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


    # Update the display
    pg.display.flip()

# Quit Pygame
pg.quit()
