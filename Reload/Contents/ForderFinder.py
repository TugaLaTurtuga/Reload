import os
import pygame as pg
import Menus

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pause = False
is_paused = True
menu_music_path = None

def un_pause_music():
    global pause, is_paused
    if pause:
        pg.mixer.music.unpause()
        is_paused = False
    else:
        pg.mixer.music.pause()
        is_paused = True
    pause = not pause

def get_music_description(path_to_folder):
    author = 'unknown'
    genre = 'unknown'
    year = '0000'

    # Get author
    author_path = os.path.join(path_to_folder, 'Author.txt')
    if os.path.exists(author_path):
        with open(author_path, 'r') as file:
            author = file.read().strip()
    else:
        with open(author_path, 'w') as file:
            file.write(author)

    # Get genre
    genre_path = os.path.join(path_to_folder, 'Genre.txt')
    if os.path.exists(genre_path):
        with open(genre_path, 'r') as file:
            genre = file.read().strip()
    else:
        with open(genre_path, 'w') as file:
            file.write(genre)

    # Get year
    year_path = os.path.join(path_to_folder, 'Year.txt')
    if os.path.exists(year_path):
        with open(year_path, 'r') as file:
            year = file.read().strip() + ' . '
    else:
        with open(year_path, 'w') as file:
            file.write(year)
        year = year + ' . '

    return author, genre, year

def play_music(music_path, folder, path_to_folder, first_time):
    global pause, menu_music_path

    print(f"Putting music on menu: {music_path.split('/')[2]}")

    author, genre, year = get_music_description(path_to_folder)
    print(f"Author: {author}")
    print(f"Genre: {genre}")
    print(f"Year: {year}")

    menu_music_path = music_path
    if menu_music_path != music_path:
        pause = not pause

    # Example of how to call Menus.__Album__ assuming it takes the correct parameters
    print("Calling Menus.__Album__ with updated details...")
    try:
        Menus.Play_album = True
        Menus.__Album__(folder, author, genre, year, path_to_folder, music_path, first_time)
    except AttributeError:
        print("Menus.__Album__ not found. Please ensure Menus defines this function.")

def render_text_with_spacing(text, font, color, letter_spacing=0):
    """Render text with custom letter spacing."""
    images = []
    width = 0

    # Render each character and calculate the total width
    for char in text:
        char_image = font.render(char, True, color)
        images.append(char_image)
        width += char_image.get_width() + letter_spacing

    # Create a surface to hold the entire text
    text_surface = pg.Surface((width, font.get_height()), pg.SRCALPHA)
    x = 0

    # Blit each character image onto the text surface
    for char_image in images:
        text_surface.blit(char_image, (x, 0))
        x += char_image.get_width() + letter_spacing

    return text_surface

def search_folders():
    album_path = os.path.expanduser('Music/Album')
    single_path = os.path.expanduser('Music/Single')

    albums = []
    singles = []

    if os.path.exists(album_path):
        albums = [f for f in os.listdir(album_path) if os.path.isdir(os.path.join(album_path, f))]

    if os.path.exists(single_path):
        singles = [f for f in os.listdir(single_path) if os.path.isdir(os.path.join(single_path, f))]

    return albums, singles

def get_folders():
    album_path = os.path.expanduser('Music/Album')
    single_path = os.path.expanduser('Music/Single')

    albums = []
    singles = []

    if os.path.exists(album_path):
        albums = [os.path.join(album_path, f) for f in os.listdir(album_path) if
                  os.path.isdir(os.path.join(album_path, f))]

    if os.path.exists(single_path):
        singles = [os.path.join(single_path, f) for f in os.listdir(single_path) if
                   os.path.isdir(os.path.join(single_path, f))]

    return albums, singles
