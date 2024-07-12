import os
import pygame as pg
from mutagen.mp3 import MP3
import ForderFinder
import SliderCode
import play_next_song
import Main_menu

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Screen settings
main_screen_width, main_screen_height, main_LeftRectwidth = 800, 600, 200
main_screen = pg.display.set_mode((main_screen_width, main_screen_height))

# Flags and initial settings
set_cursor = False
Play_album = True
start_main_menu = False
s_Album_name, s_Author, s_Genre, s_Year, s_Path_to_folder = '', '', '', '', ''
start_color = (0, 0, 0)
end_color = (25, 25, 25)

# Button settings
btns_pos = []
btns_size = []
btns_do = []
buttons_added = False

def __Menu__(screen, screen_width, screen_height, LeftRectwidth, dt):
    global main_screen_width, main_screen_height, main_LeftRectwidth, main_screen, buttons_added, current_album_name, first_timee, border_thickness, start_main_menu, album_icon_path
    main_screen = screen
    main_screen_width, main_screen_height, main_LeftRectwidth = screen_width, screen_height, LeftRectwidth
    rect = pg.Rect(LeftRectwidth / 2, 0, screen_width - (LeftRectwidth / 2), screen_height)
    pg.draw.rect(main_screen, (25, 25, 25), rect)

    if Play_album:
        down_color = start_color

        draw_gradient_rect(main_screen, main_LeftRectwidth / 2, LeftRectwidth, screen_width - main_LeftRectwidth / 2,
                           LeftRectwidth + 30, end_color, (25, 25, 25))
        if start_color != (0, 0, 0):
            SliderCode.Active_color = start_color
        __Album__(s_Album_name, s_Author, s_Genre, s_Year, s_Path_to_folder, None, False)
    else:
        if not os.path.exists(album_icon_path):
            album_icon_path = "Images/Volume/full_volume.png"
        album_icon = pg.image.load(album_icon_path)
        down_color, _ = create_contrast_color(album_icon, os.path.dirname(album_icon_path))

        if start_main_menu:
            Main_menu.start()
            start_main_menu = False
        Main_menu.Draw(dt, screen)

    count_under_50 = sum(1 for value in down_color if value < 50)
    count_under_100 = sum(1 for value in down_color if value < 50)
    if count_under_50 >= 2 and count_under_100 == 3:
        down_color = (
            min(255, down_color[0] * 4),
            min(255, down_color[1] * 4),
            min(255, down_color[2] * 4)
        )
    else:
        down_color = (
            max(0, down_color[0] // 4),
            max(0, down_color[1] // 4),
            max(0, down_color[2] // 4)
        )
    draw_gradient_rect(main_screen, main_LeftRectwidth / 2, screen_height - 100,
                       screen_width - main_LeftRectwidth / 2, 100, (25, 25, 25), down_color)

    pause_icon = make_round_icon(pg.image.load('Images/Pause.png'), 32)
    play_icon = make_round_icon(pg.image.load('Images/Play.png'), 32)

    play_x = screen_width / 2 - 16
    play_y = screen_height - 60

    if ForderFinder.is_paused:  # when paused
        main_screen.blit(play_icon, (play_x, play_y))
    else:
        main_screen.blit(pause_icon, (play_x, play_y))

    skip_x = play_x + 50
    skip_y = play_y + 5
    skip_icon =  make_round_icon(pg.image.load('Images/skip_btn.png'), 32 - 10)
    main_screen.blit(skip_icon, (skip_x, skip_y))

    back_x = play_x - 50 + 10
    back_y = play_y + 5
    back_icon = make_round_icon(pg.image.load('Images/back_btn.png'), 32 - 10)
    main_screen.blit(back_icon, (back_x, back_y))

    if not buttons_added:
        btns_pos.append((play_x, play_y))
        btns_size.append(32)
        btns_do.append(lambda: play_music(current_album_name))

        btns_pos.append((skip_x, skip_y))
        btns_size.append(32 - 10)
        btns_do.append(lambda: skip_music())

        btns_pos.append((back_x, back_y))
        btns_size.append(32 - 10)
        btns_do.append(lambda: play_next_song.play_beofre_song())

        buttons_added = True

    if (current_album_name == '' and os.path.exists('Saves/last_music.txt')):
        first_timee = True
        play_music(ForderFinder.menu_music_path)

    size = 64
    b_border_thickness = border_thickness
    border_thickness = 0
    if os.path.exists(album_icon_path):
        album_icon = make_icon(pg.image.load(album_icon_path), size)
        main_screen.blit(album_icon, (LeftRectwidth + size // 2, main_screen_height - size - 10))
    else:
        album_icon_path = 'Images/Volume/full_volume.png'
    border_thickness = b_border_thickness

    font = pg.font.Font('Fonts/Rubik/static/Rubik-Regular.ttf', 16)
    if current_album_name != '':
        tt_a = current_album_name.split('/')
        if len(tt_a[2]) > 18:
            tt_a[2] = tt_a[2][:15] + "..."
        text = font.render(tt_a[2], True, (245, 245, 245))
        textRect = text.get_rect()
        textRect.x = LeftRectwidth + size * 1.5 + 5
        textRect.y = main_screen_height - size + 10
        main_screen.blit(text, textRect)

        tt_b = os.path.dirname(current_album_name)
        tt_b = os.path.join(tt_b, 'Author.txt')
        if os.path.exists(tt_b):
            with open(tt_b, 'r') as file:
                tt_b = file.read()
        else:
            tt_b = 'unknown'

        if len(tt_b) > 10:
            first_name, second_name = tt_b.split()
            tt_b = f"{first_name} {second_name[0]}."
            if len(tt_b) > 10:
                tt_b = f"{first_name[0]}. {second_name[0]}"
                if len(tt_b) > 10:
                    tt_b = f"{first_name[3]}. {second_name[3]}."
        font = pg.font.Font('Fonts/Rubik/static/Rubik-Regular.ttf', 14)
        text = font.render(tt_b, True, (200, 200, 200))
        textRect2 = text.get_rect()
        textRect2.x = LeftRectwidth + size * 1.5 + 5 + 2
        textRect2.y = main_screen_height - size + 30
        main_screen.blit(text, textRect2)

    size = 16
    if volume_slider.value == 0:
        icon_path = 'Images/Volume/no_volume.png'
    elif 0 < volume_slider.value <= 0.3:
        icon_path = 'Images/Volume/low_volume.png'
    elif 0.3 < volume_slider.value <= 0.7:
        icon_path = 'Images/Volume/medium_volume.png'
    elif 0.8 < volume_slider.value <= 1:
        icon_path = 'Images/Volume/full_volume.png'
    else:
        icon_path = 'Images/Volume/medium_volume.png'
    icon = pg.transform.scale(pg.image.load(icon_path), (size, size))
    main_screen.blit(icon, (main_screen_width - 100 - size - 10, main_screen_height - 35 - 5))


volume_slider = SliderCode.Slider(main_screen_width - 100, main_screen_height - 35 + 5 / 2, 50, 5, 0, 1, 0.5)
music_time_slider = SliderCode.Slider(main_screen_width / 2 - 100, main_screen_height - 20 + 5 / 2, 200, 5, 0, 1, 0.5)

def skip_music():
    global new_pos
    if current_album_name != '':
        new_pos = 1
        ForderFinder.pause = True
        ForderFinder.un_pause_music()
        album = play_next_song.play_next_song()
        play_music__fisrt_time(album)

def past_music():
    play_next_song.play_beofre_song()


def change_Play_album():
    global Play_album, start_main_menu
    Play_album = not Play_album
    start_main_menu = True


def __Sliders__(screen):
    global volume_slider, music_time_slider, new_pos
    volume_slider.update_val_rect()
    volume_slider.draw(screen)
    music_time_slider.update_val_rect()
    music_time_slider.draw(screen)
    if current_album_name != '':
        music_time_slider.value = (pg.mixer.music.get_pos() / 1000 + new_pos * MP3(current_album_name).info.length) / MP3(current_album_name).info.length

        font = pg.font.Font('Fonts/Rubik/static/Rubik-Regular.ttf', 14)

        total_time_seconds = pg.mixer.music.get_pos() / 1000 + new_pos * MP3(current_album_name).info.length

        # Convert total time to hours, minutes, and seconds
        hours, remainder = divmod(total_time_seconds, 3600)
        hours = int(hours)
        minutes, seconds = divmod(remainder, 60)
        minutes, seconds = int(minutes), int(seconds)

        # Format the time as a string with proper handling of fractional seconds
        if hours > 0:
            formatted_time = '{:01.0f}:{:02.0f}:{:05.2f}'.format(hours, minutes, seconds)
        else:
            formatted_time = '{:01.0f}:{:02.0f}'.format(minutes, seconds)

        text = font.render(formatted_time, True, (245, 245, 245))
        textRect = text.get_rect()
        textRect.topright = (main_screen_width / 2 - 100 - 10, 575)
        main_screen.blit(text, textRect)

        total_max_time_seconds = MP3(current_album_name).info.length

        # Convert total time to hours, minutes, and seconds
        hours, remainder = divmod(total_max_time_seconds, 3600)
        hours = int(hours)
        minutes, seconds = divmod(remainder, 60)
        minutes, seconds = int(minutes), int(seconds)

        # Format the time as a string
        if hours > 0:
            formatted_max_time = '{:01.0f}:{:02.0f}:{:02.0f}'.format(hours, minutes, seconds)
        else:
            formatted_max_time = '{:01.0f}:{:02.0f}'.format(minutes, seconds)

        text = font.render(formatted_max_time, True, (245, 245, 245))
        textRect = text.get_rect()
        textRect.topleft = (main_screen_width / 2 + 100 + 10, 575)
        main_screen.blit(text, textRect)

        # When music ends
        if not pg.mixer.music.get_busy() and not ForderFinder.is_paused:
            new_pos = 1
            if ForderFinder.menu_music_path != current_album_name:
                play_music__fisrt_time(ForderFinder.menu_music_path)
            else:
                album = play_next_song.play_next_song()
                play_music__fisrt_time(album)

new_pos = 0
def __SLiders_event__(event, mouse):
    global volume_slider, music_time_slider, current_album_name, new_pos, start_main_menu
    volume_slider.handle_event(event)
    pg.mixer.music.set_volume(volume_slider.get_value())

    # Handle music time slider event if there is a current album playing
    if current_album_name != '':
        # Get the length of the MP3 file
        length = MP3(current_album_name).info.length

        # Get the current position of the music in seconds
        current_pos = (pg.mixer.music.get_pos() / 1000 + new_pos * length) / length

        # Handle slider events (like user interaction)
        music_time_slider.value = (pg.mixer.music.get_pos() / 1000 + new_pos * length) / length
        music_time_slider.handle_event(event)

        # Check if the new position is different from the current position and if the music is playing
        if abs(music_time_slider.get_value() - current_pos) > 1e-4:
            # Update new position
            new_pos = music_time_slider.get_value()
            # Set new music position in seconds and play from there
            pg.mixer.music.play(start=new_pos * length)
            if pg.mixer.music.get_busy():
                ForderFinder.pause = not ForderFinder.pause
                ForderFinder.un_pause_music()

    elif os.path.exists('Saves/volume.txt'):
        with open('Saves/volume.txt', 'r') as file:
            volume_slider.value = float(file.read())
    with open('Saves/volume.txt', 'w') as file:
        file.write(str(volume_slider.value))

    if not Play_album:
        if start_main_menu:
            Main_menu.start()
            start_main_menu = False
        Main_menu.handle_event(event, mouse)

play_menu_btns_pos = (0, 0)
play_menu_btns_size = 64
play_menu_btns_do = lambda: print('Nothing')


def __On_click__(mouse, event):
    global btns_pos, btns_do, btns_size, play_menu_btns_pos, play_menu_btns_size, play_menu_btns_do, start_main_menu
    for i, (btn_x, btn_y) in enumerate(btns_pos):
        if btn_x <= mouse[0] <= btn_x + btns_size[i] and btn_y <= mouse[1] <= btn_y + btns_size[i]:
            btns_do[i]()
            break
    if Play_album:
        btn_x, btn_y = play_menu_btns_pos
        if btn_x <= mouse[0] <= btn_x + play_menu_btns_size and btn_y <= mouse[1] <= btn_y + play_menu_btns_size:
            play_menu_btns_do()
    return



def __On_hover__(mouse):
    global btns_pos, btns_size, set_cursor
    set_cursor = False
    for i, (btn_x, btn_y) in enumerate(btns_pos):
        if btn_x <= mouse[0] <= btn_x + btns_size[i] and btn_y <= mouse[1] <= btn_y + btns_size[i]:
            set_cursor = True
            break

    if Play_album:
        btn_x, btn_y = play_menu_btns_pos
        if btn_x <= mouse[0] <= btn_x + play_menu_btns_size and btn_y <= mouse[1] <= btn_y + play_menu_btns_size:
            set_cursor = True
    return

top_left_color = (0,0,0)
border_color = (0,0,0)
border_thickness = 5


def make_icon(icon, size):
    global border_thickness, border_color, top_left_color

    top_left_color = icon.get_at((5, 5))

    count_under_50 = sum(1 for value in top_left_color if value < 50)
    count_under_100 = sum(1 for value in top_left_color if value < 50)
    if count_under_50 >= 2 and count_under_100 == 3:
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
    pg.draw.rect(mask, (255, 255, 255, 255), (0, 0, size, size), border_radius=4)
    if border_thickness != 0:
        bordered_size = size + 2 * border_thickness
        bordered_icon = pg.Surface((bordered_size, bordered_size), pg.SRCALPHA)
        bordered_icon.fill((0, 0, 0, 0))
        pg.draw.rect(bordered_icon, border_color, (0, 0, bordered_size, bordered_size), border_radius=4)
        bordered_icon.blit(icon, (border_thickness, border_thickness))
        return bordered_icon
    else:
        icon.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
        return icon


def make_round_icon(icon, size):
    icon = pg.transform.scale(icon, (size, size))
    mask = pg.Surface((size, size), pg.SRCALPHA)
    pg.draw.circle(mask, (255, 255, 255), (size // 2, size // 2), size // 2)
    icon.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
    return icon

def create_contrast_color(album_icon, Path_to_folder):
    album_icon.lock()
    album_color_path = os.path.join(Path_to_folder, 'color.txt')
    top_left_color = album_icon.get_at((20, 20))

    if os.path.exists(album_color_path):
        with open(album_color_path, 'r') as color_file:
            color_data = color_file.read().strip().split(',')
            start_color = (int(color_data[0]), int(color_data[1]), int(color_data[2]))
    else:
        with open(album_color_path, 'w') as color_file:
            color_data = ','.join(map(str, top_left_color))
            color_file.write(color_data)
        start_color = top_left_color

    album_icon.unlock()

    count_under_50 = sum(1 for value in start_color if value < 50)
    count_under_100 = sum(1 for value in start_color if value < 100)
    if count_under_50 >= 2 and count_under_100 == 3:
        end_color = (
            min(255, start_color[0] * 3),
            min(255, start_color[1] * 3),
            min(255, start_color[2] * 3)
        )
    else:
        end_color = (
            max(0, start_color[0] // 8),
            max(0, start_color[1] // 8),
            max(0, start_color[2] // 8)
        )

    return end_color, start_color

def draw_gradient_rect(surface, left, top, width, height, start_color, end_color):
    color_diff = (
        end_color[0] - start_color[0],
        end_color[1] - start_color[1],
        end_color[2] - start_color[2]
    )
    for y in range(height):
        color = (
            start_color[0] + (color_diff[0] * y // height),
            start_color[1] + (color_diff[1] * y // height),
            start_color[2] + (color_diff[2] * y // height)
        )
        pg.draw.line(surface, color, (left, top + y), (left + width, top + y))

first_timee = False
album_buttons_added = False
def __Album__(Album_name, Author, Genre, Year, Path_to_folder, music_path, first_time):
    global s_Album_name, s_Author, s_Genre, s_Year, s_Path_to_folder, end_color, start_color, album_buttons_added
    global first_timee, top_left_color, pause_btn
    global play_menu_btns_size, play_menu_btns_do, play_menu_btns_pos

    if first_time and not first_timee:
        first_timee = first_time

    if ForderFinder.menu_music_path == current_album_name:
        pause_btn = False
    else:
        pause_btn = True

    s_Album_name, s_Author, s_Genre, s_Year, s_Path_to_folder = Album_name, Author, Genre, Year, Path_to_folder
    size = 128

    album_icon_path = os.path.join(Path_to_folder, 'icon.png')
    if not os.path.exists(album_icon_path):
        album_icon_path = "Images/Volume/full_volume.png"
        with open(os.path.join(Path_to_folder, 'add_icon.txt'), 'w') as color_file:
            color_file.write('Add an icon by naming a image "icon.png"')
    album_icon = make_icon(pg.image.load(album_icon_path), size)

    end_color, start_color = create_contrast_color(album_icon, Path_to_folder)
    draw_gradient_rect(main_screen, main_LeftRectwidth / 2, 0, main_screen_width - main_LeftRectwidth / 2, size, start_color, end_color)
    main_screen.blit(album_icon, (main_screen_width // 3.75 - size // 2, 50))

    Album_font = pg.font.Font('Fonts/Rubik/static/Rubik-ExtraBold.ttf', 32)
    font = pg.font.Font('Fonts/Rubik/static/Rubik-Regular.ttf', 16)

    if len(Album_name) > 35:
        Album_name = Album_name[:32] + "..."
    Album_text = ForderFinder.render_text_with_spacing(Album_name, Album_font, (245, 245, 245), -1.5)
    AlbumRect = Album_text.get_rect()
    AlbumRect.x = main_screen_width // 3.75 + (size / 2) + 10
    AlbumRect.y = size - 10
    main_screen.blit(Album_text, AlbumRect)

    if len(Author) > 20:
        Author = Author[:17] + "..."
    text = font.render(Author, True, (245, 245, 245))
    textRect = text.get_rect()
    textRect.x = main_screen_width // 3.75 + (size / 2) + 16
    textRect.y = size + 25
    main_screen.blit(text, textRect)

    font = pg.font.Font('Fonts/Rubik/static/Rubik-Regular.ttf', 14)
    additional_text = '  . ' + Year + Genre
    if len(additional_text) > 35:
        additional_text = additional_text[:32] + "..."
    text = font.render(additional_text, True, (200, 200, 200))
    textRect2 = text.get_rect()
    textRect2.x = textRect.x + textRect.width
    textRect2.y = size + 25
    main_screen.blit(text, textRect2)

    big_pause_icon = make_round_icon(pg.image.load('Images/Pause.png'), 64)
    big_play_icon = make_round_icon(pg.image.load('Images/Play.png'), 64)

    play_x = (textRect2.x + textRect2.width + main_screen_height) // 1.8
    play_y = main_LeftRectwidth + 32

    if ForderFinder.pause or pause_btn:
        main_screen.blit(big_play_icon, (play_x, play_y))
    else:
        main_screen.blit(big_pause_icon, (play_x, play_y))

    play_menu_btns_pos = (play_x, play_y)
    play_menu_btns_size = 64
    play_menu_btns_do = lambda: play_music__fisrt_time(ForderFinder.menu_music_path)

def play_music__fisrt_time(music):
    global first_timee, pause_btn
    first_timee = True
    if current_album_name != music:
        play_music(music)
    else:
        ForderFinder.un_pause_music()


current_album_name = ''
album_icon_path = ''
pause_btn = True
import string
import random
length = 12
letters = string.ascii_letters
def play_music(music):
    global first_timee, current_album_name, album_icon_path, pause_btn, new_pos, Play_album
    music_folder = None
    if music is not None:
        if first_timee and current_album_name != music:
            if not pause_btn:
                print(f"Playing music: {music.split('/')[2]}")

            pg.mixer.music.load(music)
            pg.mixer.music.play()
            play_next_song.albums_already_played.append(music)
            current_album_name = music  # Update album name after loading
            new_pos = 0
            ForderFinder.pause = True
            pause_btn = False
        first_timee = False

        ForderFinder.un_pause_music()

        # Save the current music file path to 'last_music.txt'
        music_folder = os.path.dirname(music)
        with open('Saves/last_music.txt', 'w') as file:
            file.write(music)

    elif os.path.exists('Saves/last_music.txt'):
        with open('Saves/last_music.txt', 'r') as file:
            music = file.read()
        if os.path.exists(music):
            ForderFinder.menu_music_path = music
            music_folder = os.path.dirname(music)
            path_components = music.split('/')
            desired_component = path_components[2] if len(path_components) > 2 else ""
            ForderFinder.play_music(music, desired_component, music_folder, True)
        else:
            print("last_music doesn't exist, selecting random song...")
            albums, singles = ForderFinder.get_folders()
            for i in range(len(singles)):
                singles[i] = os.path.join(singles[i], 'Single.mp3')
            for i in range(len(albums)):
                albums[i] = os.path.join(albums[i], 'Album.mp3')
            s_n_a = singles + albums
            s_n_a = random.sample(s_n_a, len(s_n_a))
            music = s_n_a[0]
            print(f"Music chosen: {music}")
            with open('Saves/last_music.txt', 'w') as file:
                file.write(music)

            ForderFinder.menu_music_path = music
            music_folder = os.path.dirname(music)
            path_components = music.split('/')
            album_name = path_components[2] if len(path_components) > 2 else ""
            ForderFinder.play_music(music, album_name, music_folder, True)


    if music_folder != None:
        album_icon_path = os.path.join(music_folder, 'icon.png')
    else:
        album_icon_path = 'Images/Volume/full_volume.png'

