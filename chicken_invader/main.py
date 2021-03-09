import pygame
import sys
import time
import random

# pygame initiations
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)  # for sound
pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)

# game variables
start = False
lose = False
hold_space = False  # indicates if the spacebar is held
start_of_round = True
display_new_level = False
direction = None
score = 0
egg_chance = range(700)
start_time = -3
level = 1
num_of_waves = 1
waves_remaining = num_of_waves
health = 5
spaceship_move = 20
bullet_move = 10
egg_move = 7
chicken_x_pos = [90, 180, 270, 360, 450, 540, 630, 720, 810]
chicken_y_pos = 90
bullet_list = []
chicken_list = []
egg_list = []

# surfaces and images
bg_surface = pygame.image.load(r"images\SpaceBackground.jpg").convert()
spaceship = pygame.image.load(r"images\rocket1.png").convert_alpha()
spaceship_rect = spaceship.get_rect(center=(450, 800))
bullet = pygame.image.load(r"images\bullet.png").convert_alpha()
chicken = pygame.image.load(r"images\BigChicken.png").convert_alpha()
egg_image = pygame.image.load(r"images\Egg.png").convert_alpha()

# text and fonts
WHITE = (255, 255, 255)
RED = (255, 0, 0)
headline_font = pygame.font.SysFont("Ariel", 54)
level_font = pygame.font.SysFont("Ariel", 32)
open_screen_text = headline_font.render("Press space To Start", True, WHITE)
open_screen_rect = open_screen_text.get_rect(center=(450, 450))
new_level_text = headline_font.render("New Level", True, WHITE)
new_level_rect = new_level_text.get_rect(center=(450, 450))
lose_text = headline_font.render("You Lose", True, RED)
lose_rect = lose_text.get_rect(center=(450, 450))


def health_display(h):
    """ a function that displays the health of the player
    :param h: the players health
    :type h: int
    """
    global screen
    global level_font
    health_text = level_font.render("Health: {}".format(h), True, WHITE)
    health_text_rect = health_text.get_rect(center=(850, 850))
    screen.blit(health_text, health_text_rect)


def level_display(lv):
    """ a function that displays the level of the game
    :param lv: the game's level
    :type lv: int
    """
    global screen
    global level_font
    level_text = level_font.render("Level: {}".format(lv), True, WHITE)
    level_text_rect = level_text.get_rect(center=(850, 830))
    screen.blit(level_text, level_text_rect)


def score_display(s):
    """ a function to display the player's score
    :param s: player's score
    :type s: int
    """
    global screen
    global level_font
    score_text = level_font.render("Score: {}".format(s), True, WHITE)
    score_rect = score_text.get_rect(center=(850, 870))
    screen.blit(score_text, score_rect)


def check_collisions(rect, shot):
    """ a function to check for collisions in the game
    :param rect: a rect in the game, the chicken or spaceship
    :param shot: a bullet or an egg
    :type rect: Rect
    :type shot: Rect
    :return: true or false
    :rtype: bool
    """
    if shot.rect.colliderect(rect):
        return True
    else:
        return False


class Chicken:
    """ a class that represents all the chicken instances"""

    def __init__(self):
        """ a func that creats the attributes of each chicken"""
        self.chick = chicken
        self.rect = self.chick.get_rect(center=(0, 0))
        self.hit = False

    def chicken_placer(self, lv, x_pos, y_pos):
        """ a method that places the chicken
        :param self: the chicken instance
        :param lv: the level of the game
        :param x_pos: the position along the x axis
        :param y_pos: the position along the y axis
        :type lv: int
        :type x_pos: int
        :type y_pos: int
        """
        if lv <= 3:
            self.rect.top = lv * y_pos
            self.rect.centerx = x_pos

    def draw_chicken(self, surface):
        """ a function that draws the chicken to a surface
        :param surface: the surface of the game
        :type surface: Surface
        """
        surface.blit(self.chick, self.rect)


class Bullet:
    """a class to create a bullet instance"""

    def __init__(self, x):
        """ a function that is called when the bullet instance is made
        :param x: the x coordinate for the bullet
        :type x: int
        """
        self.bull = bullet
        self.rect = self.bull.get_rect(center=(x, 800))

    def bullet_movement(self):
        """ a method that controls the bullet movement"""
        self.rect.centery -= bullet_move


class Egg:
    """ a class for egg instances"""

    def __init__(self, x, y):
        """ a function that is called when the bullet instance is made
        :param x: the x coordinate for the egg
        :param y: the y coordinate for the egg
        :type x: int
        :type y: int
        """
        self.egg = egg_image
        self.rect = self.egg.get_rect(center=(x, y))

    def egg_movement(self):
        """ a method that controls the egg movement"""
        self.rect.centery += egg_move


while True:
    if health == 0:
        start = False
        lose = True
    screen.blit(bg_surface, (0, 0))  # fill the screen with background
    for event in pygame.event.get():  # the loop that checks for events in the game
        if event.type == pygame.QUIT:  # quits the game if the user press the x button
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not start:  # starts the game if not started
                if event.key == pygame.K_SPACE:
                    start = True
                    lose = False
            else:
                pressed = pygame.key.get_pressed()  # gets the queue of events

                # controlling the pushed buttons
                if pressed[pygame.K_LEFT] and pressed[pygame.K_RIGHT]:
                    direction = None
                    if pressed[pygame.K_SPACE] and not hold_space:
                        b = Bullet(spaceship_rect.centerx)
                        bullet_list.append(b)
                        hold_space = True
                if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                    direction = None
                    if pressed[pygame.K_SPACE] and not hold_space:
                        b = Bullet(spaceship_rect.centerx)
                        bullet_list.append(b)
                        hold_space = True
                elif (pressed[pygame.K_LEFT]) and (spaceship_rect.left - spaceship_move > 0):  # moves left
                    direction = "left"
                    if pressed[pygame.K_SPACE] and not hold_space:
                        b = Bullet(spaceship_rect.centerx)
                        bullet_list.append(b)
                        hold_space = True
                elif (pressed[pygame.K_RIGHT]) and (spaceship_rect.right + spaceship_move < 900):  # moves right
                    direction = "right"
                    if pressed[pygame.K_SPACE] and not hold_space:
                        b = Bullet(spaceship_rect.centerx)
                        bullet_list.append(b)
                        hold_space = True
                else:
                    direction = None

        # controlling when buttons are released
        if event.type == pygame.KEYUP:  # if the spacebar is released
            if event.key == pygame.K_SPACE:
                hold_space = False
            if event.key == pygame.K_LEFT and direction == "left":
                direction = None
            if event.key == pygame.K_RIGHT and direction == "right":
                direction = None

    if not start and lose == False:
        screen.blit(open_screen_text, open_screen_rect)  # open screen text display
    if not start and lose:
        screen.blit(lose_text, lose_rect)
    else:
        health_display(health)
        level_display(level)
        score_display(score)

        # spaceship movement
        if direction == "left":
            spaceship_rect.centerx -= spaceship_move
        elif direction == "right":
            spaceship_rect.centerx += spaceship_move
        screen.blit(spaceship, spaceship_rect)

        if start_of_round:  # creates the chickens at the start of a round
            for l in range(0, level):  # fill the surface with chickens
                for x in chicken_x_pos:
                    chick = Chicken()
                    chick.chicken_placer(l, x, chicken_y_pos)
                    if chick.rect.top >= 0:
                        chicken_list.append(chick)
                    chick.draw_chicken(screen)
                    start_of_round = False
        else:  # draws the chickens while in game
            for c in chicken_list:
                c.draw_chicken(screen)
                lay = random.choice(egg_chance)
                if lay == 1:  # decides if a chicken needs to lay an egg
                    x, y = c.rect.center
                    egg = Egg(x, y)
                    egg_list.append(egg)

        for b in bullet_list:  # fill the surface with bullets
            screen.blit(b.bull, b.rect)
            b.bullet_movement()

        for e in egg_list:  # fill the surface with eggs
            screen.blit(e.egg, e.rect)
            e.egg_movement()

        # check for collisions between bullets and chickens
        for c in chicken_list:
            for b in bullet_list:
                collision = check_collisions(c.rect, b)
                if collision:
                    chicken_list.remove(c)
                    bullet_list.remove(b)
                    score += 1

        # check for collisions between the eggs and the spaceship
        for e in egg_list:
            collision = check_collisions(spaceship_rect, e)
            if collision:
                egg_list.remove(e)
                health -= 1
            if e.rect.centery > 890:
                egg_list.remove(e)

        # indicates if round has ended
        if len(chicken_list) == 0:
            waves_remaining -= 1
            if waves_remaining == 0:
                screen.blit(bg_surface, (0, 0))
                bullet_list.clear()
                start_of_round = True
                level += 1
                num_of_waves = int(level / 4) + 1
                waves_remaining = num_of_waves
                start_time = time.gmtime()[5]
            else:
                for l in range(0, int(level / 4)):  # fill the surface with chickens
                    for x in chicken_x_pos:
                        chick = Chicken()
                        chick.chicken_placer(l, x, chicken_y_pos)
                        if chick.rect.top >= 0:
                            chicken_list.append(chick)
                        chick.draw_chicken(screen)

        # display new level text for 2 seconds if needed
        if time.gmtime()[5] - start_time < 2:
            if level > 1:
                screen.blit(new_level_text, new_level_rect)
        else:
            start_time = -3

    pygame.event.clear()
    pygame.display.update()
    clock.tick(90)
