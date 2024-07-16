import pygame
import json
import time
import os
import ForderFinder
import Menus
from copy import deepcopy

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Define colors
Background_color = (30, 30, 30)
Handle_color = (50, 50, 50)
Graph_color = (0, 0, 255)
Text_color = (255, 255, 255)

sensibility = 200

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, min_cursor_pos, max_cursor_pos):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.target_value = initial_val
        self.handle_width = w
        self.handle_height = h / 10
        self.handle_rect = pygame.Rect(x - (self.handle_width - w) // 2, y, self.handle_width, self.handle_height)
        self.handle_color = Handle_color
        self.rect_color = Background_color
        self.dragging = False
        self.smooth_scroll = False
        self.hovering = False
        self.min_cursor_pos, self.max_cursor_pos = min_cursor_pos, max_cursor_pos
        self.hover_timeout = time.time()  # Track the last interaction time
        self.alpha = 255
        self.update_handle_position()

    def update_handle_position(self):
        self.handle_rect.centery = self.rect.y + (self.value - self.min_val) / (self.max_val - self.min_val) * (
                    self.rect.height - self.handle_height) + self.handle_height // 2
        self.handle_rect.centerx = self.rect.centerx

    def handle_event(self, event, mouse):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                self.hover_timeout = time.time()
            elif self.rect.collidepoint(event.pos) and not self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                self.value = self.min_val + (event.pos[1] - self.rect.y) / self.rect.height * (
                            self.max_val - self.min_val)
                self.value = max(self.min_val, min(self.value, self.max_val))
                self.hover_timeout = time.time()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(event.pos) or self.handle_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            if pygame.mouse.get_pos()[0] > self.min_cursor_pos and pygame.mouse.get_pos()[0] < self.max_cursor_pos:
                self.hovering = True
                self.smooth_scroll = True
                increment = ((self.max_val / 1) / sensibility) * event.y  # Smaller value for smoother scrolling
                self.target_value = max(self.min_val, min(self.target_value - increment,
                                                          self.max_val))  # Use decrement for scroll direction
                self.hover_timeout = time.time()

        if self.hovering:
            self.hover_timeout = time.time()
        if self.dragging:
            self.smooth_scroll = False
            self.value = self.min_val + (event.pos[1] - self.rect.y) / self.rect.height * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.value, self.max_val))

    def update(self, dt):
        if self.smooth_scroll:
            self.value += (self.target_value - self.value) * dt * 10  # Adjust the speed of the animation
        self.update_handle_position()

        # Adjust alpha for fade-out effect
        if time.time() - self.hover_timeout < 1:
            self.alpha = 255
        else:
            self.alpha = max(0, self.alpha - dt * 1000)  # Adjust fade speed here

    def draw(self, screen):
        if self.hovering or self.dragging or self.smooth_scroll or self.alpha > 0:  # Draw only if the slider is visible
            # Create surfaces with alpha for fade-out effect
            rect_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            handle_surface = pygame.Surface((self.handle_rect.width, self.handle_rect.height), pygame.SRCALPHA)

            rect_color = self.rect_color + (int(self.alpha),)
            handle_color = self.handle_color + (int(self.alpha),)

            # Draw rounded rectangles on the surfaces
            pygame.draw.rect(rect_surface, rect_color, rect_surface.get_rect(), border_radius=15)
            pygame.draw.rect(handle_surface, handle_color, handle_surface.get_rect(), border_radius=15)

            # Blit the surfaces onto the screen
            screen.blit(rect_surface, self.rect.topleft)
            screen.blit(handle_surface, self.handle_rect.topleft)

    def get_value(self):
        return self.value

    def add_value(self, i):
        self.max_val = self.max_val + i
        return self.max_val

border_thickness = 4
def make_icon(image_path, size, border_radius):
    global border_thickness
    icon = pygame.image.load(image_path).convert_alpha()

    top_left_color = icon.get_at((5, 5))

    count_under_50 = sum(1 for value in top_left_color if value < 50)
    count_under_100 = sum(1 for value in top_left_color if value < 100)
    count_0 = sum(1 for value in top_left_color if value == 0)
    if count_under_50 >= 2 and count_under_100 == 3:
        border_color = (
            min(255, int(top_left_color[0] * 1.2)),
            min(255, int(top_left_color[1] * 1.2)),
            min(255, int(top_left_color[2] * 1.2))
        )
    elif count_0 != 4:
        border_color = (
            max(0, top_left_color[0] // 2),
            max(0, top_left_color[1] // 2),
            max(0, top_left_color[2] // 2)
        )
    else:
        border_color = (255, 255, 255)

    icon = pygame.transform.scale(icon, (size, size))
    mask = pygame.Surface((size, size), pygame.SRCALPHA)

    if image_path != 'Images/Volume/full_volume.png':
        pygame.draw.rect(mask, (255, 255, 255), (0, 0, size, size), border_radius=border_radius)
        icon.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    else:
        pygame.draw.rect(mask, (0, 0, 0), (0, 0, size, size), border_radius=border_radius)
        icon.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)


    # Create a surface for the border
    bordered_icon = pygame.Surface((size + 2 * border_thickness, size + 2 * border_thickness), pygame.SRCALPHA)

    # Fill the border with the border color
    bordered_icon.fill((0, 0, 0, 0))
    pygame.draw.rect(bordered_icon, border_color, (0, 0, size, size), border_radius=border_radius)

    # Blit the icon onto the bordered surface
    bordered_icon.blit(icon, (border_thickness, border_thickness))

    return bordered_icon


def get_grid():
    singles, albums = ForderFinder.get_folders()  # Assuming ForderFinder.get_folders() works correctly
    all_albums = albums + singles
    amount_of_author = []
    amount_of_genre = []
    amount_of_year = []
    A_author = {}
    A_genre = {}
    A_year = {}

    See_preferences = [1, 2, 3]  # 1 = Author, 2 = Genre, 3 = Year

    for preferences in See_preferences:
        author = 'unknown'
        genre = 'unknown'
        year = '0000'
        if preferences == 1:
            for album in all_albums:
                album_author = os.path.join(album, 'Author.txt')
                if os.path.exists(album_author):
                    with open(album_author, 'r') as file:
                        author = file.read().strip()
                if author not in A_author:
                    A_author[author] = []
                    amount_of_author.append(author)
                A_author[author].append(album)
        elif preferences == 2:
            for album in all_albums:
                album_genre = os.path.join(album, 'Genre.txt')
                if os.path.exists(album_genre):
                    with open(album_genre, 'r') as file:
                        genre = file.read().strip()
                if genre not in A_genre:
                    A_genre[genre] = []
                    amount_of_genre.append(genre)
                A_genre[genre].append(album)
        elif preferences == 3:
            for album in all_albums:
                album_year = os.path.join(album, 'Year.txt')
                if os.path.exists(album_year):
                    with open(album_year, 'r') as file:
                        year = file.read().strip()
                year = year[:-1] + '0~'
                if year not in A_year:
                    A_year[year] = []
                    amount_of_year.append(year)
                A_year[year].append(album)

    # Sort dictionaries and prepare sorted lists
    amount_of_author.sort(key=lambda x: len(A_author[x]), reverse=True)
    A_author_sorted = [A_author[author] for author in amount_of_author]

    amount_of_genre.sort(key=lambda x: len(A_genre[x]), reverse=True)
    A_genre_sorted = [A_genre[genre] for genre in amount_of_genre]

    amount_of_year = sorted(amount_of_year, reverse=True)
    A_year_sorted = [A_year[year] for year in amount_of_year]

    # Flatten lists
    flattened_A_author = [album for sublist in A_author_sorted for album in sublist]
    flattened_A_genre = [album for sublist in A_genre_sorted for album in sublist]
    flattened_A_year_sorted = [album for sublist in A_year_sorted for album in sublist]

    # Combine flattened lists
    combined_flattened_A_a = flattened_A_author + flattened_A_genre + flattened_A_year_sorted

    # Create grid_cols based on the counts of albums per author, genre, and year
    grid_cols = [len(albums) for albums in A_author_sorted + A_genre_sorted + A_year_sorted]

    return amount_of_author, amount_of_genre, amount_of_year, A_author_sorted, A_genre_sorted, A_year_sorted, combined_flattened_A_a, grid_cols


space_between_text_and_row = 25
times_text_and_row = 0
def transform_grid_cols(grid_cols, max_value=6):
    global space_between_text_and_row, times_text_and_row
    new_grid_cols = []
    add_text = []

    for value in grid_cols:
        if value <= max_value:
            new_grid_cols.append(value)
            add_text.append(True)  # Always add text for this row
            times_text_and_row += space_between_text_and_row * 1.5
        else:
            parts = value // max_value
            remainder = value % max_value

            for i in range(parts):
                new_grid_cols.append(max_value)
                if i == 0:
                    add_text.append(True)  # Add text for split part
                    times_text_and_row += space_between_text_and_row * 1.5
                else:
                    add_text.append(False)

            if remainder > 0:
                new_grid_cols.append(remainder)
                add_text.append(False)  # Don't add text immediately after the split part
    return new_grid_cols, add_text

amount_of_author, amount_of_genre, amount_of_year, A_author, A_genre, A_year, A_a, A_grid_cols = [], [], [], [], [], [], [], []
amount_of = amount_of_author + amount_of_genre + amount_of_year
slider = Slider(100, 100, 100, 100, 1, 2, 1, 1, 1)
# Define grid properties
distance_from_left = 30
distance_from_up = 30
padding = 40
cell_width = 0
cell_height = 0
border_radius = 10
font = pygame.font.Font(None, 24)

star_path = 'Images/star/On_Star.png'
star = ''

play_path = 'Images/Play.png'
play = ''

grid_cols, add_text = [], []
grid_rows = 0
max_col_number = 0

# Starting position for the grid
start_y = padding - distance_from_up

# Calculate the grid height
grid_height = 0
def start():
    global slider, star, star_path, play, play_path, cell_width, cell_height, amount_of, amount_of_author, amount_of_genre, amount_of_year, A_author, A_genre, A_year, A_a, A_grid_cols, font, button_states, button_p, json_file_path, grid_cols, add_text, grid_rows, times_text_and_row
    times_text_and_row = 0
    font = pygame.font.Font('Fonts/Rubik/static/Rubik-Bold.ttf', 24)
    amount_of_author, amount_of_genre, amount_of_year, A_author, A_genre, A_year, A_a, A_grid_cols = get_grid()
    amount_of = amount_of_author + amount_of_genre + amount_of_year
    grid_cols, add_text = transform_grid_cols(A_grid_cols, 6)
    grid_rows = len(grid_cols)
    cell_width = (Menus.main_screen_width // 6) - (80 / 6) - (distance_from_left / 2)
    cell_height = (Menus.main_screen_width // 6) - (80 / 6) - (distance_from_left / 2)
    grid_height = grid_rows * cell_height + (distance_from_up // 2) * (grid_rows - 1)

    star = pygame.image.load(star_path).convert_alpha()
    star = pygame.transform.scale(star, (cell_height // 6, cell_height // 6))

    slider = Slider(Menus.main_screen_width - 10, 0, 10, 500, 0, grid_height + cell_height - Menus.main_screen_height + times_text_and_row, 0, 80, 800)
    # Assuming A_a is defined and initialized correctly
    button_states = [[False for _ in range(col)] for col in grid_cols]
    button_p = deepcopy(button_states)

    # Load JSON data
    with open(json_file_path) as f:
        data = json.load(f)

    A_a_count = 0
    for row in range(grid_rows):
        for col in range(grid_cols[row]):
            album_path = A_a[A_a_count]
            A_a_count += 1

            # Check if album_path exists anywhere in the JSON data
            if album_path in json.dumps(data):
                button_states[row][col] = True


music_slider = Slider(0, 0, 10, 600, 0, 1, 0, 0,80)
update_music_slider = True
def __music_slider__(y_offset):
    global music_slider, update_music_slider
    if update_music_slider:
        music_slider = Slider(0, 0, 10, 600, 0, y_offset, 0, 0, 80)
        update_music_slider = False

# Store button states

json_file_path = 'Saves/Favotites.json'
button_states = []
button_p = []

# Load JSON data
if os.path.exists(json_file_path):
    with open(json_file_path) as f:
        data = json.load(f)


def handle_button_click(event, mouse_pos):
    global button_p
    times_text_and_roww = 0
    amount_of_count = 1
    A_a_count = 0
    for row in range(grid_rows):
        done_it = False
        for col in range(grid_cols[row]):  # Use range to create an iterable sequence of columns
            # Separate row by text
            if not done_it and row + 0 < len(add_text):
                if add_text[row + 0]:
                    times_text_and_roww += space_between_text_and_row * 1.5
            done_it = True

            cell_y = start_y + row * (
                    cell_width + distance_from_up // 4) + distance_from_up // 2 - slider.get_value() + times_text_and_roww
            cell_x = col * (cell_width + distance_from_left // 4) + distance_from_left // 2 + (padding * 2)

            # Blit the image in each cell
            album_path = A_a[A_a_count]
            A_a_count += 1
            cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
            if cell_rect.collidepoint(mouse_pos) and mouse_pos[1] < 500 and mouse_pos[1] < 0 and cell_y < -cell_width:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_p[row][col] == True:
                            path_components = album_path.split('/')
                            if path_components[1] == 'Album':
                                album_path = os.path.join(album_path, 'Album.mp3')
                            else:
                                album_path = os.path.join(album_path, 'Single.mp3')

                            album_folder = os.path.dirname(album_path)
                            album_name = album_path.split('/')[2]

                            # Change menus music to selected music
                            Menus.play_music__fisrt_time(album_path)
                            Menus.s_Album_name = album_name
                            Menus.s_Path_to_folder = album_folder
                            ForderFinder.menu_music_path = album_path
                            Menus.s_Author, Menus.s_Genre, Menus.s_Year = ForderFinder.get_music_description(album_folder)

                    elif event.button != 4 and event.button != 5:  # If not scrolling
                        # Change other Btns with the same album_path
                        A_a_countt = 0
                        for ro in range(grid_rows):
                            for co in range(grid_cols[ro]):  # Use range to create an iterable sequence of columns
                                album_pathh = A_a[A_a_countt]
                                A_a_countt += 1
                                if album_pathh == album_path:
                                    button_states[ro][co] = not button_states[ro][co]

                        path_components = album_path.split('/')
                        if path_components[1] == 'Album':
                            album_path = os.path.join(album_path, 'Album.mp3')
                        else:
                            album_path = os.path.join(album_path, 'Single.mp3')

                        # Check the button state
                        if button_states[row][col]:
                            print(f"Putting music on favourites: {album_path.split('/')[2]}")
                            if album_path:  # Check if album_path is valid
                                try:
                                    # Read the existing JSON file
                                    with open(json_file_path, 'r') as f:
                                        favourites = json.load(f)
                                except FileNotFoundError:
                                    # If the file doesn't exist, create an empty list
                                    favourites = []

                                # Ensure favourites is a list
                                if isinstance(favourites, str):
                                    favourites = [favourites]

                                # Add the album_path to the favourites if it's not already there
                                if album_path not in favourites:
                                    favourites.append(album_path)

                                # Write the updated favourites back to the JSON file
                                with open(json_file_path, 'w') as f:
                                    json.dump(favourites, f, indent=4)
                        else:
                            print(f"Removing music from favourites: {album_path.split('/')[2]}")
                            try:
                                # Read the existing JSON file
                                with open(json_file_path, 'r') as f:
                                    favourites = json.load(f)

                                # Ensure favourites is a list
                                if isinstance(favourites, str):
                                    favourites = [favourites]

                                # Remove the album_path from the favourites if it exists
                                if album_path in favourites:
                                    favourites.remove(album_path)

                                # Write the updated favourites back to the JSON file
                                with open(json_file_path, 'w') as f:
                                    json.dump(favourites, f, indent=4)
                            except FileNotFoundError:
                                # If the file doesn't exist, there's nothing to remove
                                pass
                elif not button_p[row][col]:
                    button_p = [[False for _ in range(col)] for col in grid_cols]
                    button_p[row][col] = True
                return
            if row == grid_rows - 1 and col == grid_cols[row] - 1:
                # Perform actions for the last row and last column
                button_p = [[False for _ in range(col)] for col in grid_cols]
                return
            if cell_y > 500:
                return


def Draw(dt, screen):
    global play, play_path
    slider.update(dt / 1000)
    # Draw the slider
    slider.draw(screen)

    # Draw the grid and text
    space_between_text_and_row = 25
    times_text_and_row = 0

    # Draw the first text always on top of the first row
    if add_text[0]:
        text_y = start_y - slider.get_value() + times_text_and_row + 10 + space_between_text_and_row
        text_between = font.render(amount_of[0], True, Text_color)
        text_between_rect = text_between.get_rect()
        text_between_rect.centery = text_y
        text_between_rect.x = 90
        screen.blit(text_between, text_between_rect)

    amount_of_count = 1
    A_a_count = 0
    for row in range(grid_rows):
        done_it = False
        for col in range(grid_cols[row]):
            if not done_it and row + 0 < len(add_text):
                if add_text[row + 0]:
                    times_text_and_row += space_between_text_and_row * 1.5
            if row + 1 < len(add_text) and not done_it:
                if add_text[row + 1]:
                    text_y = start_y + (row + 1) * (
                                cell_height + distance_from_up // 4) - slider.get_value() + space_between_text_and_row + 10 + (
                                 times_text_and_row)
                    amount_of_count += 1
                    if text_y < 500 and text_y > 0:
                        text_between = font.render(amount_of[amount_of_count - 1], True, Text_color)
                        text_between_rect = text_between.get_rect()
                        text_between_rect.centery = text_y
                        text_between_rect.x = 90
                        screen.blit(text_between, text_between_rect)
            done_it = True

            cell_y = start_y + row * (
                    cell_width + distance_from_up // 4) + distance_from_up // 2 - slider.get_value() + times_text_and_row
            cell_x = col * (cell_width + distance_from_left // 4) + distance_from_left // 2 + (padding * 2)
            if cell_y < 500:
                A_a_count += 1
                if cell_y > -cell_width:
                    # Blit the image in each cell
                    album_path = A_a[A_a_count - 1]
                    image_path = os.path.join(album_path, 'icon.png')
                    if os.path.exists(image_path):
                        image = make_icon(image_path, int(cell_width), border_radius)
                    else:
                        image = make_icon('Images/Volume/full_volume.png', int(cell_width), border_radius)
                    screen.blit(image, (cell_x, cell_y))
                    if button_states[row][col]:
                        screen.blit(star, (cell_x + cell_width * 0.8, cell_y + cell_width * 0.075))
                    if button_p[row][col]:
                        path_components = album_path.split('/')
                        if path_components[1] == 'Album':
                            album_path = os.path.join(album_path, 'Album.mp3')
                        else:
                            album_path = os.path.join(album_path, 'Single.mp3')
                        if Menus.current_album_name == album_path and not ForderFinder.is_paused:
                            play_path = 'Images/Pause.png'
                        else:
                            play_path = 'Images/Play.png'
                        play = pygame.image.load(play_path).convert_alpha()
                        play = pygame.transform.scale(play, (cell_height // 4, cell_height // 4))
                        screen.blit(play, (cell_x + cell_width * 0.75, cell_y + cell_width * 0.75))
            elif cell_y < 500:
                return

def handle_event(event, mouse_pos):
    slider.handle_event(event, mouse_pos)
    handle_button_click(event, mouse_pos)
