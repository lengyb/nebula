'''
<Lost in Darkness>
version: v1.0
date: 23/01/02
Author: BLYB
Published by Aurora Studio
Links: https://github.com/aurorastudiouk
'''

import codecs
import pygame
from pygame.locals import *  # 常量
from sys import exit
import time
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10
        self.damage = 1

    # bullet move
    def move(self):
        self.rect.top -= self.speed

    def enemies_move(self):
        self.rect.top += self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        self.image_index = 0
        self.image = player_image[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.interval = 0.2  # shoot interval
        self.interval2 = 0.05
        self.blood = 3  # player's lives

    # shoot bullet
    def shoot(self, bullet_image):
        bullet = Bullet(bullet_image, self.rect.midtop)
        self.bullets.add(bullet)

    # plane move
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0  # avoid plane out of screen
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height  # avoid plane out of screen
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0  # avoid plane out of screen
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width  # avoid plane out of screen
        else:
            self.rect.left += self.speed


# enemy plane class
class Enemy(pygame.sprite.Sprite):
    # pics   type  position
    def __init__(self, enemy_img, kind, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 1
        self.bullets = pygame.sprite.Group()  # enemy's bullets
        self.kind = kind + 1
        self.blood = kind + 1  # 3 kinds of enemies' bloof
        self.index = 0  # 坠机动画中的索引
        self.interval = 1.8  # shoot interval
        self.start = time.time()  # time enemy being created

    # enemy move
    def move(self):
        self.rect.top += self.speed

    # enemy shoot bullet
    def shoot(self, bullets_image):
        bullet = Bullet(bullets_image[self.kind - 1], self.rect.midbottom)
        bullet.damage = self.kind
        if self.kind == 1:
            bullet.speed = 5
            self.interval = 1.2
        else:
            bullet.speed = 3
        return bullet


# init pygame
pygame.init()
# init screen
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# window name
pygame.display.set_caption("Lost in Darkness")
# set window icon
icon = pygame.image.load("assets/pics/avator.png")
pygame.display.set_icon(icon)
# bg picture
background = pygame.image.load('assets/pics/background.bmp').convert()
# set background music
pygame.mixer.music.load('assets/bgm/space-adventure.wav')
pygame.mixer.music.set_volume(0.8)
# game over picture
again = pygame.image.load("assets/pics/gameover.png")
# pause
pause = pygame.image.load('assets/pics/pause.png')
# resume
resume = pygame.image.load('assets/pics/resume.png')
# player pics
player_img = []
player_img.append(pygame.image.load('assets/pics/ds_model/1.png'))
player_img.append(pygame.image.load('assets/pics/ds_model/2.png'))
player_img.append(pygame.image.load('assets/pics/ds_model/3.png'))
player_img.append(pygame.image.load('assets/pics/ds_model/4.png'))
# player weapon pics
bullet_img = pygame.image.load('assets/pics/40.png')
deadlight_img = pygame.image.load('assets/pics/24.png')
# enemy bullet
enemies_bullet_img = []
enemies_bullet_img.append(pygame.image.load('assets/pics/33.png'))
enemies_bullet_img.append(pygame.image.load('assets/pics/redball.png'))
enemies_bullet_img.append(pygame.image.load('assets/pics/supercell_lightning.png'))
# enemy plane
enemies_img = []
enemies_img.append(pygame.image.load('assets/pics/spike_model/spike1.png'))
enemies_img.append(pygame.image.load('assets/pics/supercell_model/supercell1.png'))
enemies_img.append(pygame.image.load('assets/pics/troopship_model/troopship1.png'))
# player down animation
players_down = []
for i in range(1, 5):
    img = pygame.image.load('assets/pics/ds_model/ds_explode_%s.png' % str(i))
    players_down.append(img)
# spike down
enemies1_down_img = []
enemies1_down_img.append(pygame.image.load('assets/pics/spike_model/spike_down1.png'))
enemies1_down_img.append(pygame.image.load('assets/pics/spike_model/spike_down2.png'))
enemies1_down_img.append(pygame.image.load('assets/pics/spike_model/spike_down3.png'))
# supercell down
enemies2_down_img = []
enemies2_down_img.append(pygame.image.load('assets/pics/supercell_model/supercell_down1.png'))
enemies2_down_img.append(pygame.image.load('assets/pics/supercell_model/supercell_down2.png'))
enemies2_down_img.append(pygame.image.load('assets/pics/supercell_model/supercell_down3.png'))

enemies3_down_img = []
enemies3_down_img.append(pygame.image.load('assets/pics/troopship_model/troopship_down1.png'))
enemies3_down_img.append(pygame.image.load('assets/pics/troopship_model/troopship_down2.png'))
enemies3_down_img.append(pygame.image.load('assets/pics/troopship_model/troopship_down3.png'))
enemies3_down_img.append(pygame.image.load('assets/pics/troopship_model/troopship_down4.png'))
enemies3_down_img.append(pygame.image.load('assets/pics/troopship_model/troopship_down5.png'))

enemies_down_img = []
enemies_down_img.append(enemies1_down_img)
enemies_down_img.append(enemies2_down_img)
enemies_down_img.append(enemies3_down_img)
# set game music
# leaderboard sound
rangking_sound = pygame.mixer.Sound("assets/bgm/epics-inspiring.wav")
rangking_sound.set_volume(0.8)
# new record sound
new_record_sound = pygame.mixer.Sound("assets/bgm/effect/instakill.mp3")
new_record_sound.set_volume(2)
# player laser sound
player_shoot = pygame.mixer.Sound('assets/bgm/effect/darkstar-laser00.mp3')
player_shoot.set_volume(0.5)
player_deadlight = pygame.mixer.Sound('assets/bgm/effect/deadlight.mp3')
player_deadlight.set_volume(0.3)
# game over sound
over_sound = pygame.mixer.Sound('assets/bgm/effect/game_over.mp3')
over_sound.set_volume(2)

enemy3_shoot = pygame.mixer.Sound('assets/bgm/effect/redball.wav')
enemy3_shoot.set_volume(0.3)
# explosion
plane_collision = pygame.mixer.Sound('assets/bgm/effect/kill.wav')
plane_collision.set_volume(1.5)
# reborn sound
reborn_sound = pygame.mixer.Sound('assets/bgm/effect/reborn.mp3')
# clap sound
clap_sound = pygame.mixer.Sound('assets/bgm/effect/clapfox.mp3')
clap_sound.set_volume(0.4)


# read high score from file
def readScores(path):
    with open(path, 'r', encoding="utf8") as f:
        lines = f.readlines()
    return lines


# write score into file
def writeScores(context, srtim, path):
    f = codecs.open(path, srtim, "utf8")
    f.write(str(context))
    f.close()

# game over
def gameOver(scores):
    x = screen.get_rect().centerx
    y = screen.get_rect().centery
    # restart
    start = pygame.font.Font(None, 45)
    start_text = start.render("New Battle", True, (90, 160, 100))
    start_rect = start_text.get_rect()
    start_rect.centerx = x
    start_rect.centery = y + 40
    screen.blit(start_text, start_rect)

    # show game final score
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Scores: %s" % str(scores), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y - 50
    screen.blit(text, text_rect)

    # leaderboard
    text = start.render("Legends", True, (90, 160, 100))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y + 130
    screen.blit(text, text_rect)

    # update leaderboard info
    scores_array = readScores(r'score.txt')[0].split('mr')

    if scores >= int(scores_array[2]):
        start = pygame.font.Font(None, 70)
        text = start.render("YOU ARE ON FIRE!!!", True, (255, 0, 0))
        pygame.mixer.Sound.stop(over_sound)
        pygame.mixer.Sound.play(new_record_sound)
        text_rect = text.get_rect()
        text_rect.centerx = x
        text_rect.centery = y - 160
        screen.blit(text, text_rect)

    temp = 0
    for i in range(0, len(scores_array)):
        if scores > int(scores_array[i]):
            temp = int(scores_array[i])
            scores_array[i] = str(scores)
            scores = 0
        if temp > int(scores_array[i]):
            k = int(scores_array[i])
            scores_array[i] = str(temp)
            temp = k

    # start write scores
    for i in range(0, len(scores_array)):
        if i == 0:
            writeScores(scores_array[i] + 'mr', 'w', 'score.txt')
        elif i == 9:
            writeScores(str(scores_array[i]), 'a', 'score.txt')
        else:
            writeScores(scores_array[i] + 'mr', 'a', 'score.txt')


# show score in game
def showScores(scores):
    myfont = pygame.font.Font(None, 30)
    text = myfont.render("Scores: %s" % str(scores), True, (0,255,255))
    screen.blit(text, (650, 550))
    pygame.display.update()


# show pause
def showPaused():
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Paused", True, (250, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery
    screen.blit(text, text_rect)
    pygame.display.update()


# show leaderboard
def gameRanking():
    screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen2.fill(0)
    screen2.blit(background, (0, 0))

    x = screen.get_rect().centerx
    y = screen.get_rect().centery
    # show text on leaderboard
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Legends", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 50
    screen.blit(text, text_rect)

    # restart
    start = pygame.font.Font(None, 45)
    start_text = start.render("New Battle", True, (90, 160, 100))
    start_rect = start_text.get_rect()
    start_rect.centerx = x
    start_rect.centery = y + 40
    screen.blit(start_text, start_rect)

    # get scores from file
    scores_array = readScores(r'score.txt')[0].split('mr')
    # rank gold
    text = start.render("Gold: %s" % scores_array[0], True, (255,215,0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 150
    screen.blit(text, text_rect)

    # rank silver
    text = start.render("Silver: %s" % scores_array[1], True, (220,220,220))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 200
    screen.blit(text, text_rect)

    # rank bronze
    text = start.render("Bronze: %s" % scores_array[2], True, (255,128,0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 250
    screen.blit(text, text_rect)


# start game
def startGame():
    pygame.display.set_caption("Lost in Darkness")
    pygame.mixer.Sound.stop(rangking_sound)
    pygame.mixer.Sound.stop(clap_sound)
    pygame.mixer.Sound.play(reborn_sound)
    scores = 0  # your scores
    player_pos = [350, 400]
    enemy_pos = [[random.randint(0, 200), -200], [random.randint(200, 400), -200], [random.randint(400, 600), -200]]
    player = Player(player_img, player_pos)

    global running  # judge if game is running
    running = True
    global is_paused  # judge if game is paused
    is_paused = False
    start = time.time()
    change_times = 1  # plane change times
    arrive_times = 1  # enemy arrive times
    enemies_bomb = 1  # enemy bomb times
    bomb_times = 0.04  # plane bomb animation
    enemies = pygame.sprite.Group()  # enemy group
    enemies_down = pygame.sprite.Group()  # enemy down group
    enemies_bullet = pygame.sprite.Group()  # enemy bullet group

    # game main loop
    while running:
        # music loop
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        screen.fill(0)
        screen.blit(background, (0, 0))  # set bg
        if is_paused == False:
            screen.blit(pause, (575, 525))  # shown pause button
        else:
            screen.blit(resume, (575, 525))  # shown resume button
        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and running:
                # pause
                if 575 <= event.pos[0] and event.pos[0] <= 625 and 605 >= event.pos[1] and event.pos[1] >= 525:
                    is_paused = True if is_paused == False else False
        # pause function
        if is_paused:
            showPaused()
            continue;

        if not player.is_hit:
            screen.blit(player.image, player.rect)
            if change_times % 55 == 0 and player.blood == 3:
                player.image_index = 1 if player.image_index % 2 == 0 else 0
                player.image = player_img[player.image_index]
                change_times = 0
            # if player hit, change image
            elif change_times % 55 == 0 and player.blood < 3:
                player.image_index = 1 if player.image_index % 2 == 0 else 0
                if player.image_index == 1:
                    player.image = players_down[0]
                else:
                    player.image = player_img[player.image_index]
                change_times = 0
            change_times += 1

        # generate enemy
        if arrive_times % 100 == 0:
            type = random.randint(0, len(enemies_img) - 1)
            pos = random.randint(0, len(enemies_img) - 1)
            enemy = Enemy(enemies_img[type], type, enemy_pos[2 - pos])
            enemies.add(enemy)
            arrive_times = 1
        arrive_times += 1

        # enemy move
        for enemy in enemies:
            enemy.move()
            if time.time() - enemy.start > enemy.interval:
                if enemy.kind == 1:
                    player_shoot.play()
                else:
                    enemy3_shoot.play()
                enemies_bullet.add(enemy.shoot(enemies_bullet_img))
                enemy.start = time.time()
            #delete enemy
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
            # enemy hit
            if pygame.sprite.collide_rect(enemy, player):
                enemies.remove(enemy)
                player.is_hit = True
                break
            enemy.bullets.draw(screen)

        for enemy_bullet in enemies_bullet:
            enemy_bullet.enemies_move()
            if enemy_bullet.rect.top > SCREEN_HEIGHT:
                enemies_bullet.remove(enemy_bullet)
            if pygame.sprite.collide_rect(enemy_bullet, player):
                enemies_bullet.remove(enemy_bullet)
                player.blood -= enemy_bullet.damage
            if player.blood <= 0:
                player.blood = 0
                player.is_hit = True
        enemies_bullet.draw(screen)

        if player.is_hit:
            plane_collision.play()
            pygame.mixer.music.stop()
            over_sound.play()
            temp_time = time.time()

            j = 0
            while True:
                if time.time() - temp_time > bomb_times:
                    screen.blit(players_down[j], player.rect)
                    temp_time = time.time()
                    if j == len(players_down) - 1:
                        running = False
                        break
                    j += 1
        enemies.draw(screen)

        # get key pressed
        key_pressed = pygame.key.get_pressed()
        # move
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
        # shoot
        if key_pressed[K_SPACE] and time.time() - start >= player.interval:
            player.shoot(bullet_img)
            player_shoot.play()
            start = time.time()
       #######################################################
        if key_pressed[K_x] and time.time() - start >= player.interval2:
            player.shoot(deadlight_img)
            player_deadlight.play()
            start = time.time()

        # get bullet back
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # draw bullet
        player.bullets.draw(screen)

        for enemy in enemies:
            for bullet in player.bullets:
                # collision
                if pygame.sprite.collide_rect(enemy, bullet):
                    player.bullets.remove(bullet)
                    enemy.blood -= bullet.damage
                    # if enemy blood is 0, delete enemy
                    if enemy.blood <= 0:
                        enemies_down.add(enemy)
                        plane_collision.play()
                        scores += enemy.kind * 10
                    else:
                        enemy.image = enemies_down_img[enemy.kind - 1][enemy.index]
                        enemy.index += 1
        # show score
        showScores(scores)

        # show bomb of enemy
        for enemy in enemies_down:
            if enemies_bomb % 5 == 0:
                enemy.image = enemies_down_img[enemy.kind - 1][enemy.index]
                enemy.index += 1
                enemies_bomb = 0
            if enemy.index == len(enemies_down_img[enemy.kind - 1]):
                enemies.remove(enemy)
                enemies_down.remove(enemy)
        enemies_bomb += 1
        pygame.display.update()  # refresh screen

    # show final score
    if not is_paused:
        gameOver(scores)


# let's play
startGame()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # judge if mouse cliked
        elif event.type == pygame.MOUSEBUTTONDOWN and not running and not is_paused:
            x = screen.get_rect().centerx
            y = screen.get_rect().centery
            # restart
            if x - 100 <= event.pos[0] and event.pos[0] <= x + 100 and y + 70 >= event.pos[1] and event.pos[1] >= y + 40:
                startGame()

            # show the leaderboard
            if x - 120 <= event.pos[0] and event.pos[0] <= x + 120 and y + 160 >= event.pos[1] and event.pos[1] >= y + 130:
                pygame.mixer.music.stop()
                rangking_sound.play()  # play leaderboard bgm
                pygame.display.set_caption('Legends')
                pygame.mixer.Sound.play(clap_sound)
                gameRanking()

    pygame.display.update()
