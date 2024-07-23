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

    print(f"Putting music on menu: {music_path.split('/')[3]}")

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
        Menus.__Album__(music_path.split('/')[3], author, genre, year, path_to_folder, music_path, first_time)
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
    album_path = os.path.expanduser('../Music/Album')
    single_path = os.path.expanduser('../Music/Single')

    albums = []
    singles = []

    if os.path.exists(album_path):
        albums = [f for f in os.listdir(album_path) if os.path.isdir(os.path.join(album_path, f))]

    if os.path.exists(single_path):
        singles = [f for f in os.listdir(single_path) if os.path.isdir(os.path.join(single_path, f))]

    return albums, singles

def get_folders():
    album_path = os.path.expanduser('../Music/Album')
    single_path = os.path.expanduser('../Music/Single')

    albums = []
    singles = []

    if os.path.exists(album_path):
        albums = [os.path.join(album_path, f) for f in os.listdir(album_path) if
                  os.path.isdir(os.path.join(album_path, f))]

    if os.path.exists(single_path):
        singles = [os.path.join(single_path, f) for f in os.listdir(single_path) if
                   os.path.isdir(os.path.join(single_path, f))]

    return albums, singles

def get_music_file(path):
    music = ''
    if os.path.exists(path):
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        music_files = [
            os.path.join(path, f) for f in files if
            f.endswith('.mp3') or f.endswith('.MP3') or
            f.endswith('.aac') or f.endswith('.AAC') or
            f.endswith('.wav') or f.endswith('.WAV') or
            f.endswith('.flac') or f.endswith('.FLAC') or
            f.endswith('.alac') or f.endswith('.ALAC') or
            f.endswith('.ogg') or f.endswith('.OGG') or
            f.endswith('.aiff') or f.endswith('.AIFF') or
            f.endswith('.aif') or f.endswith('.AIF') or
            f.endswith('.wma') or f.endswith('.WMA') or
            f.endswith('.dts') or f.endswith('.DTS') or
            f.endswith('.ape') or f.endswith('.APE') or
            f.endswith('.mpc') or f.endswith('.MPC') or
            f.endswith('.wv') or f.endswith('.WV') or
            f.endswith('.mid') or f.endswith('.MID') or
            f.endswith('.midi') or f.endswith('.MIDI') or
            f.endswith('.amr') or f.endswith('.AMR') or
            f.endswith('.3gp') or f.endswith('.3GP') or
            f.endswith('.m4a') or f.endswith('.M4A') or
            f.endswith('.opus') or f.endswith('.OPUS') or
            f.endswith('.mp2') or f.endswith('.MP2') or
            f.endswith('.ra') or f.endswith('.RA') or
            f.endswith('.rm') or f.endswith('.RM') or
            f.endswith('.au') or f.endswith('.AU') or
            f.endswith('.snd') or f.endswith('.SND') or
            f.endswith('.bwf') or f.endswith('.BWF') or
            f.endswith('.tta') or f.endswith('.TTA') or
            f.endswith('.dsd') or f.endswith('.DSD') or
            f.endswith('.cda') or f.endswith('.CDA') or
            f.endswith('.voc') or f.endswith('.VOC') or
            f.endswith('.vqf') or f.endswith('.VQF') or
            f.endswith('.spx') or f.endswith('.SPX') or
            f.endswith('.caf') or f.endswith('.CAF') or
            f.endswith('.mus') or f.endswith('.MUS') or
            f.endswith('.gsm') or f.endswith('.GSM') or
            f.endswith('.dss') or f.endswith('.DSS') or
            f.endswith('.m3u') or f.endswith('.M3U') or
            f.endswith('.m3u8') or f.endswith('.M3U8') or
            f.endswith('.pls') or f.endswith('.PLS') or
            f.endswith('.asx') or f.endswith('.ASX') or
            f.endswith('.ram') or f.endswith('.RAM') or
            f.endswith('.rmi') or f.endswith('.RMI')
        ]

        if music_files:
            music = music_files[0]

    return music