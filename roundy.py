"""
This is an original design of Denniel Luis S. Sadian
from Gasan, Marinduque, Philippines on August 5, 2017
"""

import pygame
import sys
import os
import random
import json


def load_png(name):
    """
    For loading PNGs
    :param name: full name of the PNG
    :return: tuple
    """
    fullname = os.path.join('resources', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        raise SystemExit(f'Cannot load image: {fullname}')
    return image, image.get_rect()


def play_sound(name):
    """
    For playing a sound
    :param name:
    :return:
    """
    fullname = os.path.join('resources', name)
    sound = pygame.mixer.Sound(fullname)
    sound.play()


def message(msg, color, where, size='small'):
    if size is 'small':
        screen.blit(small_font.render(msg, True, color), where)
    elif size is 'medium':
        screen.blit(medium_font.render(msg, True, color), where)
    elif size is 'large':
        screen.blit(large_font.render(msg, True, color), where)


class Roundy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = pics['happy']
        self.x = 120
        self.y = 205
        self.lead_y = 3
        self.location_y = int()
        self.score = int()

    def go_up(self):
        roundy.image = pics['oh'][0]
        self.location_y = self.y - 45
        self.lead_y = -5

    def move(self):
        self.y += self.lead_y
        if self.y <= 0 or self.y+30 >= 500:
            self.image = pics['sad'][0]
            self.lead_y = 0
        if self.y <= self.location_y:
            self.lead_y = 3
        screen.blit(self.image, (self.x, self.y))


class Ghost(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = pics['ghost']
        self.x = random.randint(600, 2000)
        self.y = random.randint(20, 420)
        self.area_y = (self.y-20, self.y)
        self.lead_y = -1
        self.location_x = (self.x, self.x+50)
        self.location_y = (self.y, self.y+60)

    def hover(self, speed):
        self.x += -speed
        self.y += self.lead_y
        if self.y <= self.area_y[0]:
            self.lead_y = 1
        if self.y >= self.area_y[1]:
            self.lead_y = -1
        if self.x <= -50:
            roundy.score += 2
            self.__init__()
        screen.blit(self.image, (self.x, self.y))

    def harmed(self, other):
        if other.x <= self.x+5 <= other.x+30 <= self.x+50 or self.x <= other.x <= self.x+45:
            if other.y+30 >= self.y+60 >= other.y and other.y <= self.y+60:
                play_sound('electricity.wav')
                return True
            elif other.y+30 >= self.y >= other.y and other.y <= self.y+60:
                play_sound('electricity.wav')
                return True


# initialization
if os.path.exists('resources/high_score.txt'):
    with open('resources/high_score.txt', 'r') as hs:
        high_score = json.load(hs)[0]
else:
    with open('resources/high_score.txt', 'w') as hs:
        json.dump([0], hs)
    high_score = 0
pygame.init()
width = 600
height = 500
screen = pygame.display.set_mode((width, height))
screen.fill((200, 225, 235))
small_font = pygame.font.SysFont('comicsansms', 25)
medium_font = pygame.font.SysFont('comicsansms', 50)
large_font = pygame.font.SysFont('comicsansms', 70)
pics = {'happy': load_png('roundy_happy.png'),
        'sad': load_png('roundy_sad.png'),
        'oh': load_png('roundy_oh.png'),
        'ghost': load_png('ghost.png'),
        'icon': load_png('window_icon.png'),
        1: load_png('day.png'), 2: load_png('night.png'),
        3: load_png('space.png')}
pygame.display.set_icon(pics['icon'][0])
pygame.display.set_caption('Roundy the Circle!')

roundy = Roundy()
ghost = Ghost()
ghost1 = Ghost()
ghost2 = Ghost()
ghost3 = Ghost()
ghost4 = Ghost()
ghost5 = Ghost()
ghost6 = Ghost()
ghost7 = Ghost()
ghost8 = Ghost()
ghost9 = Ghost()

setting = random.randint(1, 3)
lead_x = -1
x = 0
clock = pygame.time.Clock()


def introduction():

    global setting, lead_x, x, high_score
    speed = 2
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        mouse = pygame.mouse.get_pos()

        if roundy.x < mouse[0] < roundy.x+30 and roundy.y < mouse[1] < roundy.y+30:
            roundy.image = pics['oh'][0]
        else:
            roundy.image = pics['happy'][0]

        x += lead_x
        if x <= -600:
            setting = random.randint(1, 3)
            x = 0

        screen.blit(pics[setting][0], (x, 0))
        ghost.hover(speed)
        ghost1.hover(speed)
        ghost2.hover(speed)
        ghost3.hover(speed)
        ghost4.hover(speed)
        ghost5.hover(speed)
        ghost6.hover(speed)
        ghost7.hover(speed)
        ghost8.hover(speed)
        ghost9.hover(speed)
        screen.blit(roundy.image, (roundy.x, roundy.y))
        message(f'High Score: {high_score}', (200, 0, 0), (15, 450))
        message('Welcome to Roundy!', (0, 200, 0), (70, 30), 'medium')
        message('Do not let him cry', (0, 0, 200), (200, 200))
        message('Careful with the ghosts, they multiply', (0, 0, 200), (85, 250))
        message('Space to play, Q to quit, P to pause', (0, 0, 200), (100, 300))

        pygame.display.update()
        clock.tick(60)


def game_loop():

    global setting, lead_x, x, high_score

    crashed = False
    game_over = False
    paused = False
    speed = 2

    ghost.__init__()
    ghost1.__init__()
    ghost2.__init__()
    ghost3.__init__()
    ghost4.__init__()
    ghost5.__init__()
    ghost6.__init__()
    ghost7.__init__()
    ghost8.__init__()
    ghost9.__init__()
    roundy.__init__()

    while not crashed:

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        setting = random.randint(1, 3)
                        game_loop()
            x += lead_x
            if x <= -600:
                x = 0
            roundy.image = pics['sad'][0]
            screen.blit(roundy.image, (roundy.x, roundy.y))
            message(f'Score: {roundy.score}', (0, 200, 0), (5, 0), 'medium')
            message(f'High Score: {high_score}', (0, 200, 0), (15, 70))
            message('Game Over :(', (200, 0, 0), (90, 100), 'large')
            message('Space play again, Q to quit', (0, 0, 200), (150, 250))
            pygame.display.update()
            clock.tick(60)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        paused = False
                    elif event.key == pygame.K_p:
                        paused = False
            message(f'Score: {roundy.score}', (0, 200, 0), (5, 0), 'medium')
            message(f'High Score: {high_score}', (0, 200, 0), (15, 70))
            message('Paused', (200, 0, 0), (190, 100), 'large')
            message("Don't keep Roundy waiting", (0, 0, 200), (150, 250))
            pygame.display.update()
            clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    roundy.go_up()
                elif event.key == pygame.K_p:
                    paused = True
            elif event.type == pygame.KEYUP:
                roundy.image = pics['happy'][0]

        x += lead_x
        if x <= -600:
            x = 0

        screen.blit(pics[setting][0], (x, 0))
        ghost.hover(speed)
        ghost1.hover(speed)
        ghost2.hover(speed)
        ghost3.hover(speed)
        ghost4.hover(speed)
        roundy.move()

        if roundy.score >= 100:
            ghost5.hover(speed)
        if roundy.score >= 200:
            ghost6.hover(speed)
        if roundy.score >= 300:
            ghost7.hover(speed)
        if roundy.score >= 400:
            ghost8.hover(speed)
        if roundy.score >= 500:
            ghost9.hover(speed)
        if roundy.score % 10 is 0 and roundy.score is not 0:
            speed += 0.10
            roundy.score += 2

        if roundy.score > high_score:
            high_score = roundy.score
            with open('resources/high_score.txt', 'w') as h:
                json.dump([high_score], h)

        message(f'Score: {roundy.score}', (0, 200, 0), (5, 0), 'medium')
        message(f'High Score: {high_score}', (0, 200, 0), (15, 70))

        if ghost.harmed(roundy) or ghost1.harmed(roundy) or ghost2.harmed(roundy):
            play_sound('game_over.wav')
            game_over = True
        if ghost3.harmed(roundy) or ghost4.harmed(roundy) or ghost5.harmed(roundy):
            play_sound('game_over.wav')
            game_over = True
        if ghost6.harmed(roundy) or ghost7.harmed(roundy) or ghost8.harmed(roundy):
            play_sound('game_over.wav')
            game_over = True
        if ghost9.harmed(roundy):
            play_sound('game_over.wav')
            game_over = True

        if roundy.y <= 0 or roundy.y+30 >= 500:
            play_sound('game_over.wav')
            game_over = True

        pygame.display.update()
        clock.tick(60)


introduction()
game_loop()
