import os, ForderFinder, Menus
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

albums_played = ['']
current_genre = ''
albums_already_played = []
def play_next_song():
    global albums_played
    print('Playing next music / Skipping music')
    albums, singles = ForderFinder.get_folders()
    current_genre = Menus.s_Genre
    all_genre_albums = []
    all_author_albums = []
    all_albums = []
    albums_played.append(Menus.current_album_name)

    # Play next album by genre
    for album in albums:
        Genre_path = os.path.join(album, 'Genre.txt')
        album_path = album
        all_albums.append(ForderFinder.get_music_file(album_path))

    # Play next single by genre
    for single in singles:
        Genre_path = os.path.join(single, 'Genre.txt')
        single_path = single
        all_albums.append(ForderFinder.get_music_file(single_path))

    all_albums = random.sample(all_albums, len(all_albums))

    print("Trying songs with same genre... ")
    for album in all_albums:
        album_path = os.path.dirname(album)
        Genre_path = os.path.join(album_path, 'Genre.txt')
        if os.path.exists(Genre_path):
            with open(Genre_path, 'r') as file:
                Genre = file.read()
            if Genre == Menus.s_Genre and album != Menus.current_album_name:
                play = True
                for played in albums_played:
                    if played == album:
                        play = False
                if play:
                    all_genre_albums.append(album)
                    albums_played.append(album)
                    print("Try nº: 1 succeeded")
                    return album

    print("No more songs available in the selected genre. Trying others with same author... "
          "Try nº: 1 failed")
    # open all all_albums and check if 'Author.txt' == s_Author
    for album in all_albums:
        album_path = os.path.dirname(album)
        Author_path = os.path.join(album_path, 'Author.txt')
        if os.path.exists(Author_path):
            with open(Author_path, 'r') as file:
                Author = file.read()
            if Author == Menus.s_Author and album != Menus.current_album_name:
                play = True
                for played in albums_played:
                    if played == album:
                        play = False
                if play:
                    all_author_albums.append(album)
                    albums_played.append(album)
                    print("Try nº: 2 succeeded")
                    current_genre = Genre
                    return album

    print("No more songs available in the selected author. Trying others with same genre but replayed... "
          "Try nº: 2 failed")
    albums_played = []
    albums_played.append(Menus.current_album_name)
    for album in all_albums:
        album_path = os.path.dirname(album)
        Genre_path = os.path.join(album_path, 'Genre.txt')
        if os.path.exists(Genre_path):
            with open(Genre_path, 'r') as file:
                Genre = file.read()
            if Genre == Menus.s_Genre and album != Menus.current_album_name:
                all_genre_albums.append(album)
                albums_played.append(album)
                print("Try nº: 3 succeeded")
                return album

    print("No more songs available in the selected genre. Trying others with same author but replayed..."
          "Try nº: 3 failed")
    for album in all_albums:
        album_path = os.path.dirname(album)
        Author_path = os.path.join(album_path, 'Author.txt')
        if os.path.exists(Author_path) and album != Menus.current_album_name:
            with open(Author_path, 'r') as file:
                Author = file.read()
            if Author == Menus.s_Author:
                all_author_albums.append(album)
                albums_played.append(album)
                print("Try nº: 4 succeeded")
                return album

    print("No more songs available. Trying a ramdom album that isn't the one being played..."
          "Try nº: 4 failed")
    for album in all_albums:
        if album != Menus.current_album_name:
            albums_played.append(album)
            print("Try nº: 5 succeeded")
            return album
        
    print("No more songs available. Playing the same album..."
          "failed")
    return Menus.current_album_name


def play_beofre_song():
    if len(albums_already_played) > 0:
        if albums_already_played[len(albums_already_played) - 2] != '' and albums_already_played[len(albums_already_played) - 2] != Menus.current_album_name:
            print(f"Music currently being played: {Menus.current_album_name.split('/')[2]}")
            album = albums_already_played[len(albums_already_played) - 2]
            print(f"Changing it to: {album.split('/')[2]}")
            Menus.pause_btn = True
            Menus.play_music__fisrt_time(album)
            del albums_already_played[len(albums_already_played) - 2]
            del albums_already_played[len(albums_already_played) - 1]
        else:
            print(f"Could´n find any songs played before: {Menus.current_album_name.split('/')[2]}")
    return
