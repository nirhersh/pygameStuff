import pygame
import sys
import random
import pandas
import openal

# game's initial variables
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((800, 900))
clock = pygame.time.Clock()


# different screens
bg_surface = pygame.image.load(r"open_screen.jpg").convert()
lose_screen = pygame.image.load(r"lose_screen.jpg").convert()
victory_screen = pygame.image.load(r"victory_screen.jpg").convert()

# data frame for grid
grid_df = pandas.read_excel("battleships_grid.xlsx")
grid_df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

# variables for ship placer function
char_to_num = {}
num_to_char = {}
num_of_column = 0
for character in grid_df.columns:
    char_to_num[character] = num_of_column
    num_of_column += 1
num_of_column = 0
for character in grid_df.columns:
    num_to_char[num_of_column] = character
    num_of_column += 1

# other game variables
ship_sizes = [2, 2, 3, 4, 4, 5]
block_size = 80
grid_height = 800
grid_width = 800
start = False
display_error_text = False
win = False
ammo = 30

# sounds in game
hit_sound = openal.oalOpen(r'sounds/cannon.wav')
miss_sound = openal.oalOpen(r'sounds/water.wav')

# rectangles for the grid
game_rects = []
for x in range(grid_width // block_size):
    for y in range(grid_height // block_size):
        rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
        game_rects.append(rect)

# texts and fonts
headline_font = pygame.font.SysFont("Ariel", 54)
lower_font = pygame.font.SysFont("Ariel", 24)
open_screen_text = headline_font.render("Press Any Key To Start", True, (0, 0, 0))
text_rect = open_screen_text.get_rect(center=(400, 600))
already_guessed_text = lower_font.render("You already tried that one", True, (255, 0, 0))
error_text_rect = already_guessed_text.get_rect(center=(400, 820))
you_lose_text = headline_font.render("You Lose!", True, (255, 0, 0))
you_lose_rect = you_lose_text.get_rect(center=(400, 500))


def draw_grid(height, width, block):
    """ a function that draws the grid fo the game
    :param height: window's height
    :param width: window's width
    :param block: the size of a block in the game
    :type height, width, block: int
    :return: None"""
    for x in range(width // block + 1):
        for y in range(height // block + 1):
            pygame.draw.line(screen, (255, 0, 0), (x * block, y * block), (800, y * block))
            pygame.draw.line(screen, (255, 0, 0), (x * block, y * block), (x * block, 800))
    return


def ship_placer(df, ship_size, list_of_ships):
    """ a function that places the ships randomly on the grid, 0 means no ship, 1 means ship placed
    :param df: the grid's dataframe
    :param ship_size: the num of blocks the ship has
    :param list_of_ships: the list of the remaining ships to place
    :type df: panda's dataframe
    :type ship_size: int
    :type list_of_ships: list
    :return: None
    """
    global char_to_num
    global num_to_char  # the two dicts that help to transform numbers to character and vice versa
    placement_valid = True  # a variable to dictate if the position is valid for placement
    column_names = df.columns
    ship_y_pos = random.choice(range(10))
    ship_x_pos = random.choice(column_names)
    ship_direction = random.choice(['x', 'y'])  # ship's direction, horizontal for x and vertical for y
    if ship_direction == 'x':
        ship_end = char_to_num[ship_x_pos] + ship_size  # the ship's end position
        if ship_end > 9:  # must'nt exceed the df
            return
        else:
            for column in range(char_to_num[ship_x_pos], ship_end):
                column = num_to_char[column]
                if df.loc[ship_y_pos, column] == 1:
                    placement_valid = False  # this block checks if a ship is already placed in the position
            if placement_valid:
                for column in range(char_to_num[ship_x_pos], ship_end):
                    column = num_to_char[column]
                    df.at[ship_y_pos, column] = 1  # this block places the ship
            else:
                return
    else:
        ship_end = ship_y_pos + ship_size
        if ship_end > 9:
            return
        else:
            for index in range(ship_y_pos, ship_end):
                if df.loc[index, ship_x_pos] == 1:
                    placement_valid = False
            if placement_valid:
                for index in range(ship_y_pos, ship_end):
                    df.at[index, ship_x_pos] = 1
            else:
                return
    list_of_ships.remove(ship_size)  # removes the placed ship for the list of ships
    return


def check_rect(mouse, list_of_rects, df):
    """ a function that checks if the player clicked on a ship. 0 means no ship, 1 means ship, 2 means hit, 3 means miss
    :param mouse: the position of the mouse when clicked
    :param list_of_rects: list of rectangles on the grid
    :param df: the grid's dataframe
    :type mouse: tuple
    :type list_of_rects: list
    :type df: DataFrame
    :return: an integer and the rectangle hit or false
    :rtype: list or bool
    """
    global char_to_num
    global num_to_char
    global ammo
    for rectan in list_of_rects:
        if rectan.collidepoint(mouse):
            rec_pos_x = int(rectan.left / 80)
            rec_pos_x = num_to_char[rec_pos_x]
            rec_pos_y = int(rectan.top / 80)
            print(rec_pos_y, rec_pos_x)
            if df.at[rec_pos_y, rec_pos_x] == 1:
                df.at[rec_pos_y, rec_pos_x] = 2
                hit_sound.play()
                ammo -= 1
                return True
            elif df.at[rec_pos_y, rec_pos_x] == 0:
                df.at[rec_pos_y, rec_pos_x] = 3
                miss_sound.play()
                ammo -= 1
                return True
            elif (df.at[rec_pos_y, rec_pos_x] == 2) or (df.at[rec_pos_y, rec_pos_x] == 3):
                return False


def rect_painter(df, list_of_rects):
    """ a function that paints the rectangle on the grid according to the dataframe values
    :param df: the grid dataframes
    :param list_of_rects: a list of rectangles
    :type df: DataFrame
    :type list_of_rects: list
    """
    global char_to_num
    global num_to_char
    for rectangle in list_of_rects:
        rec_pos_x = int(rectangle.left / 80)
        rec_pos_x = num_to_char[rec_pos_x]
        rec_pos_y = int(rectangle.top / 80)
        if df.at[rec_pos_y, rec_pos_x] == 2:
            pygame.draw.rect(screen, (255, 0, 0), rectangle)
        elif df.at[rec_pos_y, rec_pos_x] == 3:
            pygame.draw.line(screen, (255, 0, 0), (rectangle.left, rectangle.top), (rectangle.left + 80, rectangle.top + 80))
            pygame.draw.line(screen, (255, 0, 0), (rectangle.left, rectangle.top + 80), (rectangle.left + 80, rectangle.top))
    return


def check_win(df):
    """ a function that checks if there are any not destroyed ships in game
    :param df: the grid dataframe
    :type df: panda's DataFrame
    :return: true or false
    :rtype: bool
    """
    for i in df.itertuples():
        if 1 in i[1:]:
            return False
    return True


while True:
    for event in pygame.event.get():  # the loop that checks for events in the game
        if event.type == pygame.QUIT:  # quits the game if the user press the x button
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not start:
            start = True
        if event.type == pygame.MOUSEBUTTONDOWN and start and not win:
            mouse_pos = pygame.mouse.get_pos()
            check = check_rect(mouse_pos, game_rects, grid_df)
            if not check:
                display_error_text = True
            else:
                display_error_text = False

    if not start:
        screen.blit(bg_surface, (0, 0))
        screen.blit(open_screen_text, text_rect)
    elif start:
        if len(ship_sizes) > 0:
            for ship in ship_sizes:
                ship_placer(grid_df, ship, ship_sizes)
        print(grid_df)
        win = check_win(grid_df)
        if (ammo == 0) and (not win):
            screen.blit(lose_screen, (0, 0))
            screen.blit(you_lose_text, you_lose_rect)
        elif win:
            screen.blit(victory_screen, (0, 0))
        else:
            screen.fill(color=(0, 0, 255))
            ammo_left_text = lower_font.render("Ammo left: {}".format(ammo), True, (255, 0, 0))
            ammo_text_rect = ammo_left_text.get_rect(center=(400, 870))
            screen.blit(ammo_left_text, ammo_text_rect)
            draw_grid(grid_height, grid_width, block_size)
            rect_painter(grid_df, game_rects)

            if display_error_text:
                screen.blit(already_guessed_text, error_text_rect)

    pygame.display.update()
    clock.tick(20)
