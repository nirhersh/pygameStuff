import pygame
import sys
import random
import openal
import timer

# game variables
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 30)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# dashed lines variables
y_line_coord = 0
x_line_coord = 500
line_length = 35
list_of_y = []
for y in range(0, 20):
    if y % 2 == 0:
        y_line_coord = y_line_coord + 70
        list_of_y.append(y_line_coord)
    else:
        continue

# players rectangles
player_1 = pygame.Rect((0, 300), (25, 100))
player_2 = pygame.Rect((975, 300), (25, 100))
ball = pygame.Rect((488, 338), (25, 25))

# some more variables
move_1 = None  # use to store the next movements of the players
move_2 = None
start = False
first_start = True
movements_2 = (pygame.K_UP, pygame.K_DOWN)
movements_1 = (pygame.K_w, pygame.K_s)
horizontal_directions = ('left', 'right')
vertical_directions = ('up', 'down')
vertical = None
horizontal = None
out_of_screen = False
player_1_score = 0
player_2_score = 0
x_change = 10
y_change = 10

# text and font
headline_font = pygame.font.SysFont("Ariel", 54)
open_screen_text = headline_font.render("Press space To Start", True, WHITE)
open_screen_rect = open_screen_text.get_rect(center=(500, 350))

# sounds
paddle_hit = openal.oalOpen(r"sounds/paddle_hit.wav")
wall_hit = openal.oalOpen(r"sounds/wall_hit.wav")

# images
speed_mushroom = pygame.image.load(r"pictures/speed.png").convert_alpha()
growth_mushroom = pygame.image.load(r"pictures/growth.png").convert_alpha()
mushrooms = [speed_mushroom, growth_mushroom]


def move_up(rectangle):
    """ a function to move a player's rectangle up the screen
    :param rectangle: the rectangle of the player
    :type rectangle: Rect
    :return: None
    """
    if rectangle.y - 30 > -30:
        rectangle.y -= 30


def move_down(rectangle):
    """ a function to move a player's rectangle down the screen
    :param rectangle: the rectangle of the player
    :type rectangle: Rect
    :return: None
    """
    if rectangle.y + 30 < 630:
        rectangle.y += 30


def ball_movement(vertical_direct, horizontal_direct, collision=False, out=False):
    """ a function that controls the ball movement
    :param vertical_direct: the vertical direction of the ball
    :param horizontal_direct: the horizontal direction of the ball
    :param collision: indicates if the ball collided with a players rectangle
    :param out: indicates if the ball is out of screen
    :type vertical_direct: str
    :type horizontal_direct: str
    :type collision: bool
    :type out: bool
    :return: returns the updates vertical and horizontal directions and if the ball is out of screen
    """
    global x_change
    global y_change
    ver = vertical_direct
    hor = horizontal_direct
    if vertical_direct == 'up':
        if ball.y - y_change > 0:
            ball.y -= y_change
        else:
            if collision:
                change = random.choice((4, -4))
                if change == 4:
                    if y_change + change < 14:
                        y_change += change
                else:
                    if y_change + change < 6:
                        y_change += change
                ver = 'down'
    else:
        if ball.y + y_change < 700:
            ball.y += y_change
        else:
            if collision:
                change = random.choice((4, -4))
                if change == 4:
                    if y_change + change < 14:
                        y_change += change
                else:
                    if y_change + change < 6:
                        y_change += change
                ver = 'up'

    if horizontal_direct == 'left':
        if ball.x + x_change < 970:
            ball.x += x_change
        else:
            if collision:
                change = random.choice((4, -4))
                if change == 4:
                    if y_change + change < 14:
                        y_change += change
                else:
                    if y_change + change < 6:
                        y_change += change
                hor = 'right'
            else:
                out = True
    else:
        if ball.x - x_change > 0:
            ball.x -= x_change
        else:
            if collision:
                change = random.choice((4, -4))
                if change == 4:
                    if y_change + change < 14:
                        y_change += change
                else:
                    if y_change + change < 6:
                        y_change += change
                hor = 'left'
            else:
                out = True
    return ver, hor, out


def check_collisions(player1, player2, game_ball):
    """ a function that checks if there was a collision between a player's rect and the ball
    :param player1: player 1 rect
    :param player2: player 2 rect
    :param game_ball: ball rect
    :type player1, player2, game_ball: rect
    :return col: a variable that indicates if there was a collision
    :rtype: bool
    """
    col = False
    if game_ball.colliderect(player1) or game_ball.colliderect(player2):
        paddle_hit.play()
        col = True
    elif game_ball.centery >= 670 or game_ball.centery <= 20:
        wall_hit.play()
        col = True
    return col


def draw_players(player_one, player_two):
    """ a function that draws the players rectangles to the screen
    :param player_one: player one rectangle
    :param player_two: player two rectangle
    :type player_one: Rect
    :type player_two: Rect
    :return: None
    """
    pygame.draw.rect(screen, WHITE, player_one)
    pygame.draw.rect(screen, WHITE, player_two)


def score_update(score_1, score_2, direction, out=False):
    """ a function that updates the scores of the players
    :param score_1: the score of player 1
    :param score_2:the score of player 2
    :param direction: the last direction horizontally"of the ball
    :param out: indicates if the ball is out of the game
    :type score_1: int
    :type score_2: int
    :type direction: str
    :type out: bool
    :return: score 1 and score 2
    :rtype: int
    """
    if out:
        if direction == 'left':
            score_1 += 1
        else:
            score_2 += 1
    player_1_text = headline_font.render("{}".format(score_1), True, WHITE)
    player_2_text = headline_font.render("{}".format(score_2), True, WHITE)
    score_rect_1 = player_1_text.get_rect(center=(350, 200))
    score_rect_2 = player_2_text.get_rect(center=(650, 200))
    screen.blit(player_1_text, score_rect_1)
    screen.blit(player_2_text, score_rect_2)
    return score_1, score_2


def acceleration_func(timer_id, time):
    """ a function that accelerates the speed of the ball as long as he is in the game
    :param timer_id: the id of the game timer
    :param time: the time the timer counted
    :type timer_id: timer
    """
    global x_change
    x_change += 0.01
    timer.kill_timer(timer_id)


def draw_mushrooms(timer_id, time):
    global mushrooms
    shroom = random.choice(mushrooms)
    x_shroom = random.choice(range(100, 900))
    y_shroom = random.choice(range(100, 600))
    shroom_rect = shroom.get_rect(center=(x_shroom, y_shroom))
    screen.blit(shroom, shroom_rect)
    timer.kill_timer(timer_id)




while True:
    screen.fill(BLACK)
    score_update(player_1_score, player_2_score, horizontal)

    if not start:
        screen.blit(open_screen_text, open_screen_rect)

    for y_coord in list_of_y:
        pygame.draw.line(screen, WHITE, (x_line_coord, y_coord - 35), (x_line_coord, y_coord))

    draw_players(player_1, player_2)

    if start:
        if first_start:
            first_start = False
            vertical, horizontal, out_of_screen = ball_movement(random.choice(vertical_directions),
                                                                random.choice(horizontal_directions))
            pygame.draw.rect(screen, WHITE, ball)
        else:
            pygame.draw.rect(screen, WHITE, ball)
            vertical, horizontal, out_of_screen = ball_movement(vertical, horizontal,
                                                                check_collisions(player_1, player_2, ball), out_of_screen)
            if out_of_screen:
                x_change = 10
                player_1_score, player_2_score = score_update(player_1_score, player_2_score, horizontal, out_of_screen)
                ball.center = (500, 350)
                pygame.draw.rect(screen, WHITE, ball)
                vertical, horizontal, out_of_screen = ball_movement(random.choice(vertical_directions), horizontal)

    pygame.display.update()
    t = timer.set_timer(4000, acceleration_func)
    mushroom_timer = timer.set_timer(4000, draw_mushrooms)

    clock.tick(80)

    for event in pygame.event.get():  # the loop that checks for events in the game
        if event.type == pygame.QUIT:  # quits the game if the user press the x button
            openal.oalQuit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not start:
                if event.key == pygame.K_SPACE:
                    start = True
            else:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP]:
                    move_2 = pygame.K_UP
                if pressed[pygame.K_DOWN]:
                    move_2 = pygame.K_DOWN
                if pressed[pygame.K_w]:
                    move_1 = pygame.K_w
                if pressed[pygame.K_s]:
                    move_1 = pygame.K_s
                if pressed[pygame.K_ESCAPE]:
                    start = False
                    ball.center = (488, 338)
                    player_1_score = 0
                    player_2_score = 0

                if move_2 == pygame.K_UP:
                    move_up(player_2)
                elif move_2 == pygame.K_DOWN:
                    move_down(player_2)

                if move_1 == pygame.K_w:
                    move_up(player_1)
                elif move_1 == pygame.K_s:
                    move_down(player_1)

                move_1 = None
                move_2 = None
