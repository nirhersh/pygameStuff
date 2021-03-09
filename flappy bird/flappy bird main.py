import pygame
import sys
import random


def draw_floor():
    """ a function that draws the floor over and over again to make it look continues"""
    screen.blit(floor_surface, (floor_x_position, 900))
    screen.blit(floor_surface, (floor_x_position + 576, 900))


def create_pipe():
    """a function that creates the pipes at random positions throughout the game"""
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    """a function that moves the x positions of the pipes to make it look continues
    :param pipes: the pipes that the game created
    :type pipes: list
    """
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    """ the function that draws the pipe to the game, and flips half of them
    :param pipes: the pipes that the game created
    :type pipes: list
    """
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collisions(pipes):
    """ a function that checks if the bird collided with a pipe or the limits of the screen
    :param pipes: the pipes that the game created
    :type pipes: list
    """
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True


def rotate_bird(bird):
    """ a function that rotates the bird according to its movement
    :param bird: the bird surface to rotate
    :type bird: Surface
    """
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    """ a function that switches between the bird surfaces to make it look like it flaps its wings"""
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    """ a function that displays the score and the highscore at the end of the game
    :param game_state: a paramater that indicates the state of the game
    :type game_state: string
    """
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    """ a function that updates the highest score if needed
    :param score: the score that was achieved in the current game
    :param high_score: the highest score that was achieved
    :type score: int
    :type high_score: int
    """
    if score > high_score:
        high_score = score
    return high_score


# game variables
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# background
bg_surface = pygame.image.load(r"assets/background-day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# floor
floor_surface = pygame.image.load(r"assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

# bird variables
bird_downflap = pygame.transform.scale2x(pygame.image.load(r"assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(r"assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(r"assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# pipes variables
pipe_surface = pygame.image.load(r"assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# game over variables
game_over_surface = pygame.transform.scale2x(pygame.image.load(r"assets/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

# sounds
flap_sound = pygame.mixer.Sound(r'sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound(r'sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound(r'sound/sfx_point.wav')
score_sound_countdown = 100

# the game loop
while True:
    for event in pygame.event.get():  # the loop that checks for events in the game
        if event.type == pygame.QUIT:  # quits the game if the user press the x button
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:  # makes the bird jump if the user press space
                bird_movement = 0
                bird_movement -= 9
                flap_sound.play()
            if (event.key == pygame.K_SPACE) and (game_active == False):  # restarts the game if the user press space
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:  # spawns a new pipe every time the spawn pipe timer ends
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:  # triggers the bird animation function when the birdflap timer ends
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))  # draws the background of the game to the screen

    if game_active:
        # bird stuff
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collisions(pipe_list)

        # pipe stuff
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1

        if score_sound_countdown <= 0:  # triggers the score sound when the score changes
            score_sound.play()
            score_sound_countdown = 100

    # draws the game over screen
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # floor stuff
    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0
    screen.blit(floor_surface, (floor_x_position, 900))
    pygame.display.update()
    clock.tick(80)
