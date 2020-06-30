import gettext
import math
import random
import sys
from time import sleep

import pygame
from pygame.locals import *

window_width = 800
window_height = 600

black = (0, 0, 0)
white = (200, 200, 200)
yellow = (250, 250, 20)
blue = (20, 20, 250)

pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('2019250063 길효민 : 암석 피하기 게임')
pygame.display.set_icon(pygame.image.load('warp.png'))
fps_clock = pygame.time.Clock()
fps = 60
score = 0

d_font = pygame.font.Font('NanumGothic.ttf', 28)
back_img = pygame.image.load('background.jpg')
ex_sound = pygame.mixer.Sound('explosion.wav')
warp_sound = pygame.mixer.Sound('warp.wav')
pygame.mixer.music.load('Inner_Sanctum.mp3')

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super(Spaceship, self).__init__()
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
    
    def set_pos(self, x, y):
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

    
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Rock, self).__init__()
        rocks = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png',
                'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png',
                'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png',
                'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png',
                'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png',
                'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png',)

        self.image = pygame.image.load(random.choice(rocks))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    def set_direction(self):
        if self.hspeed > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            self.image = pygame.transform.rotate(self.image, 180)


    def update(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        if self.collide():
            self.kill()

    def collide(self):
        if self.rect.x < 0 - self.rect.height or self.rect.x > window_width:
            return True
        elif self.rect.y < 0 - self.rect.height or self.rect.y > window_height:
            return True


def random_rock(speed):
    random_direction = random.randint(1, 4)
    if random_direction == 1:
        return Rock(random.randint(0, window_width), 0, 0, speed)
    elif random_direction == 2:
        return Rock(window_width, random.randint(0, window_height), -speed, 0)
    elif random_direction == 3:
        return Rock(random.randint(0, window_width), window_height, 0, -speed)
    elif random_direction == 4:
        return Rock(0, random.randint(0, window_height), speed, 0)


class Warp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Warp, self).__init__()
        self.image = pygame.image.load('warp.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.centery

def draw_back(background_img):
    background_rect = background_img.get_rect()
    for i in range(int(math.ceil(window_width / background_rect.width))):
        for j in range(int(math.ceil(window_height / background_rect.height))):
            screen.blit(background_img, Rect(i * background_rect.width,
                                            j * background_rect.height,
                                            background_rect.width,
                                            background_rect.height))


def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

def game_loop():
    global score

    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(False)

    spaceship = Spaceship()
    spaceship.set_pos(*pygame.mouse.get_pos())
    rocks = pygame.sprite.Group()
    warps = pygame.sprite.Group()

    min_rock_speed = 1
    max_rock_speed = 1
    occur_of_rocks = 1
    occur_prob = 15
    score = 0
    warp_count = 1
    paused = False

    while True:
        pygame.display.update()
        fps_clock.tick(fps)

        if paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        pygame.mouse.set_visible(False)
                if event.type == QUIT:
                    return 'quit'
        else:
            draw_back(back_img)

            occur_of_rocks = 1 + int(score / 500)
            min_rock_speed = 1 + int(score / 400)
            max_rock_speed = 1 + int(score / 300)

            if random.randint(1, occur_prob) == 1:
                for i in range(occur_of_rocks):
                    rocks.add(random_rock(random.randint(min_rock_speed, max_rock_speed)))
                    score += 1

                if random.randint(1, occur_prob * 10) == 1:
                    warp = Warp(random.randint(30, window_width - 30),
                                random.randint(30, window_height - 30))
                    warps.add(warp)

            draw_text('점수 : {}'.format(score), d_font, screen, 80, 20, yellow)
            draw_text('워프 : {}'.format(warp_count), d_font, screen, 700, 20, blue)
            rocks.update()
            warps.update()
            rocks.draw(screen)
            warps.draw(screen)

            warp = spaceship.collide(warps)

            if spaceship.collide(rocks):
                ex_sound.play()
                pygame.mixer.music.stop()
                rocks.empty()
                return 'game_screen'
            elif warp:
                warp_count += 1
                warp.kill()

            screen.blit(spaceship.image, spaceship.rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] <= 10:
                        pygame.mouse.set_pos(window_width - 10, mouse_pos[1])
                    elif mouse_pos[0] >= window_width - 10:
                        pygame.mouse.set_pos(0 + 10, mouse_pos[1])
                    elif mouse_pos[1] <= 10:
                        pygame.mouse.set_pos(mouse_pos[0], window_height - 10)
                    elif mouse_pos[1] >= window_height - 10:
                        pygame.mouse.set_pos(mouse_pos[0], 0 + 10)
                    spaceship.set_pos(*mouse_pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if warp_count > 0:
                        warp_count -= 1
                        warp_sound.play()
                        sleep(1)
                        rocks.empty()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            transp_surf = pygame.Surface((window_width, window_height))
                            transp_surf.set_alpha(150)
                            screen.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            draw_text('일시정지',
                                        pygame.font.Font('NanumGothic.ttf', 60),
                                        screen, window_width / 2, window_height / 2, yellow)
                if event.type == QUIT:
                    return 'quit'

    return 'game_screen'
        

def game_screen():
    global score
    pygame.mouse.set_visible(True)

    start_image = pygame.image.load('game_screen.png')
    screen.blit(start_image, [0, 0])

    draw_text('암석 피하기', pygame.font.Font('NanumGothic.ttf', 70), screen,
                window_width / 2, window_height / 3.4, white)
    draw_text('점수 : {}'.format(score), 
                d_font, screen,
                window_width / 2, window_height / 2.4, yellow)
    draw_text("마우스 버튼이나 'S'키를 누르면 게임이 시작됩니다.", 
                d_font, screen,
                window_width / 2, window_height / 2.0, yellow)
    draw_text("게임을 종료하려면 'Q'키를 누르세요.",
                d_font, screen,
                window_width / 2, window_height / 1.8, yellow)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return 'quit'
            elif event.key == pygame.K_s:
                return 'play'
        if event.type == pygame.MOUSEBUTTONDOWN:
            return 'play'
        if event.type == QUIT:
            return 'quit'

    return 'game_screen'

def main_loop():
    action = 'game_screen'
    while action != 'quit':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'play':
            action = game_loop()
    
    pygame.quit()


main_loop()
