import codecs, pygame, random, time
from pygame.locals import *

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)

pygame.init()
clock = pygame.time.Clock()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, side, init_pos, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.speed = 10
        self.damage = 1
        if side == 'left':
            self.rect.left = player.rect.left + 5
            self.rect.top = player.rect.top
        elif side == 'right':
            self.rect.right = player.rect.right - 5
            self.rect.top = player.rect.top
        elif side == 'middle':
            self.rect.midbottom = init_pos

    def move(self):
        self.rect.top -= self.speed
    def enemies_move(self):
        self.rect.top += self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, player_image,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        self.finished = False
        self.image_index = 0
        self.image = player_image[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.interval = 0.2
        self.blood = 5
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, 'left', (0, 0), self)
        bullet2 = Bullet(bullet_img, 'right', (0, 0), self)
        self.bullets.add(bullet, bullet2)
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
    def reset(self):
        self.rect.topleft = [200, 600]
        self.bullets = pygame.sprite.Group()
        self.is_hit = False

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
        self.blood = kind + 1  # 3 kinds of enemies' blood
        self.index = 0
        self.interval = 3 # shoot interval
        self.start = time.time()  # time enemy being created
    def move(self):
        self.rect.top += self.speed
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
    def shoot(self, bullets_image):
        bullet = Bullet(bullets_image[self.kind - 1], 'middle', self.rect.midbottom, self)
        self.bullets.add(bullet)
        bullet.damage = self.kind
        if self.kind == 1:
            bullet.speed = 5
            self.interval = 3
        else:
            bullet.speed = 3
        return bullet

class Meteor(pygame.sprite.Sprite):
    def __init__(self, meteor_img, kind, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 1
        self.kind = kind + 1
        self.index = 0
        self.start = time.time()
    def move(self):
        self.rect.top += self.speed

class Gem(pygame.sprite.Sprite):
    def __init__(self, gem_img, kind, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = gem_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 1
        self.kind = kind + 1
        self.index = 0
        self.start = time.time()
    def move(self):
        self.rect.top += self.speed


pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Polaris | Zero_")
icon = pygame.image.load('resource/avator.png')
pygame.display.set_icon(icon)
# bg picture
background = pygame.image.load('resource/bg1.jpg')
# BGM

# logo sound
logo_sound = pygame.mixer.Sound('resource/OST/space-logo.wav')
logo_sound.set_volume(0.8)
# game over picture
again = pygame.image.load('resource/bg1_blur.png')
# player pics
player_img = []
player_img.append(pygame.image.load('resource/ds_model/ds_1.png'))
player_img.append(pygame.image.load('resource/ds_model/ds_2.png'))
player_img.append(pygame.image.load('resource/ds_model/ds_3.png'))
player_img.append(pygame.image.load('resource/ds_model/ds_4.png'))

# enemy bullet
enemies_bullet_img = []
enemies_bullet_img.append(pygame.image.load('resource/bullet_model/33.png'))
enemies_bullet_img.append(pygame.image.load('resource/bullet_model/redball.png'))
enemies_bullet_img.append(pygame.image.load('resource/bullet_model/supercell_lightning.png'))
# enemy plane
enemies_img = []
enemies_img.append(pygame.image.load('resource/spike_model/spike1.png'))
enemies_img.append(pygame.image.load('resource/supercell_model/supercell1.png'))
enemies_img.append(pygame.image.load('resource/troopship_model/troopship1.png'))
# meteor
meteors_img = []
meteors_img.append(pygame.image.load('resource/meteor/1.png'))
meteors_img.append(pygame.image.load('resource/meteor/2.png'))
meteors_img.append(pygame.image.load('resource/meteor/3.png'))
# gem
gems_img = []
gems_img.append(pygame.image.load('resource/gem/1.png'))
gems_img.append(pygame.image.load('resource/gem/2.png'))
gems_img.append(pygame.image.load('resource/gem/3.png'))
#menu img
menu_img = pygame.image.load('resource/menu.jpg')

# player down animation
players_down = []
for i in range(1, 5):
    img = pygame.image.load('resource/ds_model/ds_down%s.png' % str(i))
    players_down.append(img)
# spike down
enemies1_down_img = []
enemies1_down_img.append(pygame.image.load('resource/spike_model/spike_down1.png'))
enemies1_down_img.append(pygame.image.load('resource/spike_model/spike_down2.png'))
enemies1_down_img.append(pygame.image.load('resource/spike_model/spike_down3.png'))
# supercell down
enemies2_down_img = []
enemies2_down_img.append(pygame.image.load('resource/supercell_model/supercell_down1.png'))
enemies2_down_img.append(pygame.image.load('resource/supercell_model/supercell_down2.png'))
enemies2_down_img.append(pygame.image.load('resource/supercell_model/supercell_down3.png'))

enemies3_down_img = []
enemies3_down_img.append(pygame.image.load('resource/troopship_model/troopship_down1.png'))
enemies3_down_img.append(pygame.image.load('resource/troopship_model/troopship_down2.png'))
enemies3_down_img.append(pygame.image.load('resource/troopship_model/troopship_down3.png'))
enemies3_down_img.append(pygame.image.load('resource/troopship_model/troopship_down4.png'))
enemies3_down_img.append(pygame.image.load('resource/troopship_model/troopship_down5.png'))

enemies_down_img = []
enemies_down_img.append(enemies1_down_img)
enemies_down_img.append(enemies2_down_img)
enemies_down_img.append(enemies3_down_img)
# leaderboard sound
rangking_sound = pygame.mixer.Sound("resource/OST/galaxy.wav")
rangking_sound.set_volume(0.8)
# new record sound
new_record_sound = pygame.mixer.Sound('resource/sounds/instakill.mp3')
new_record_sound.set_volume(1)
# player laser sound
bullet_sound = pygame.mixer.Sound('resource/sounds/laser.mp3')
# game over sound
click_sound = pygame.mixer.Sound('resource/sounds/game_over.mp3')
click_sound.set_volume(1)
# explosion
plane_collision = pygame.mixer.Sound('resource/sounds/kill.wav')
plane_collision.set_volume(1)
# re-born sound
reborn_sound = pygame.mixer.Sound('resource/sounds/reborn.mp3')
reborn_sound.set_volume(1)

# menu metoer img
bg_metoer_img = []
bg_metoer_img.append(pygame.image.load('resource/bg_metoer.png'))

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

# menu
def menu(scores):
    pygame.mixer.music.load('resource/OST/challenging-orchestra.wav')
    pygame.mixer.music.play(-1, 0.0)
    x = screen.get_rect().centerx
    y = screen.get_rect().centery
    screen.blit(menu_img, (0, 0))
    myfont = pygame.font.Font(None, 60)
    sentence = ("Polaris | Nebula")
    count = 0
    while count <= len(sentence):
        text = myfont.render(sentence[:count], True, (0,0,0))
        screen.blit(text, (x-150 , y - 100))
        pygame.display.update()
        pygame.time.delay(100)
        count += 1

    start = pygame.font.Font(None, 45)
    start_text = start.render("Journey", True, (255,255,255))
    start_rect = start_text.get_rect()
    start_rect.centerx = x
    start_rect.centery = y + 100
    screen.blit(start_text, start_rect)

    text = start.render("Memoir", True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y + 50
    screen.blit(text, text_rect)

    # exit game
    exit_text = start.render("Escape", True, (255,255,255))
    exit_rect = exit_text.get_rect()
    exit_rect.centerx = x
    exit_rect.centery = y + 150
    screen.blit(exit_text, exit_rect)
    #

    # update leaderboard info
    scores_array = readScores(r'score.txt')[0].split('mr')

    if scores >= int(scores_array[2]):
        start = pygame.font.Font(None, 70)
        text = start.render("Apex Round !", True, (255, 0, 0))
        pygame.mixer.Sound.play(new_record_sound)
        text_rect = text.get_rect()
        text_rect.centerx = x
        text_rect.centery = y - 150
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

# show pause
def showPaused():
    screen.blit(again, (0, 0))
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Paused", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery
    screen.blit(text, text_rect)
    pygame.display.update()

# show leaderboard
def gameRanking():
    screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen2.fill(0)
    screen2.blit(again, (0, 0))
    x = screen.get_rect().centerx
    y = screen.get_rect().centery
    # show text on leaderboard
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Apex", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 250
    screen.blit(text, text_rect)

    # restart
    start = pygame.font.Font(None, 45)
    start_text = start.render("New Game", True, (255, 0, 0))
    start_rect = start_text.get_rect()
    start_rect.centerx = x
    start_rect.centery = y + 100
    screen.blit(start_text, start_rect)

    # get scores from file
    scores_array = readScores(r'score.txt')[0].split('mr')
    # 1
    text = start.render("1st: %s" % scores_array[0], True, (248,248,255))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 300
    screen.blit(text, text_rect)

    # 2
    text = start.render("2st: %s" % scores_array[1], True, (248,248,255))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 350
    screen.blit(text, text_rect)

    # 3
    text = start.render("3st: %s" % scores_array[2], True, (248,248,255))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 400
    screen.blit(text, text_rect)

def loading():
    pygame.init()
    loading_img = pygame.image.load('resource/loading/%s.jpg' % random.randint(1, 3))
    screen3 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.update()
    screen3.fill(0)
    screen3.blit(loading_img, (0, 0))
    pygame.display.update()
    pygame.time.delay(5000)


# start game
def startGame():
    pygame.display.set_caption("Journey")
    pygame.mixer.Sound.stop(rangking_sound)
    pygame.mixer.Sound.play(reborn_sound)
    scores = 0  # your scores

    player_pos = [925, 700]  # player position
    player = Player(player_img, player_pos)  # player object
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
    meteors = pygame.sprite.Group()  # meteor group
    gems = pygame.sprite.Group()  # gem group

    # game main loop
    while running:
        # music loop
        if not pygame.mixer.music.get_busy():

           pygame.mixer.music.load('resource/OST/%s.wav' % random.randint(1, 6))
           pygame.mixer.music.set_volume(1.5)
           pygame.mixer.music.play()
        screen.fill(0)
        screen.blit(background, (0, 0))  # set bg

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
                    if is_paused:
                        showPaused()
                    else:
                        pygame.display.update()
        # pause function
        if is_paused:
            showPaused()
            continue;

        if not player.is_hit:
            screen.blit(player.image, player.rect)
            if change_times % 55 == 0 and player.blood == 6:
                player.image_index = 1 if player.image_index % 2 == 0 else 0
                player.image = player_img[player.image_index]
                change_times = 0
            # if player hit, change image
            elif change_times % 55 == 0 and player.blood < 5:
                player.image_index = 1 if player.image_index % 2 == 0 else 0
                if player.image_index == 1:
                    player.image = players_down[0]
                else:
                    player.image = player_img[player.image_index]
                change_times = 0
            change_times += 1
        # generate enemy
        if arrive_times % 50 == 0 and scores <= 3000:
            type = random.randint(0, len(enemies_img) - 1)
            enemy_pos = [random.randint(0, SCREEN_WIDTH - enemies_img[type].get_width()), 0]
            enemy = Enemy(enemies_img[type], type, enemy_pos)
            enemies.add(enemy)
        # generate meteor
        if arrive_times % 50 == 0 and scores > 1000 and scores <= 3000:
            type2 = random.randint(0, len(meteors_img) - 1)
            meteor_pos = [random.randint(0, SCREEN_WIDTH - meteors_img[type2].get_width()), 0]
            meteor = Meteor(meteors_img[type2], type2, meteor_pos)
            meteors.add(meteor)
            arrive_times = 1
        arrive_times += 1
        if arrive_times >= 100:
            arrive_times = 0
        # generate gem
        if arrive_times % 50 == 0:
            type3 = random.randint(0, len(meteors_img) - 1)
            gem_pos = [random.randint(0, SCREEN_WIDTH - gems_img[type3].get_width()), 0]
            gem = Meteor(gems_img[type3], type3, gem_pos)
            gems.add(gem)
            arrive_times = 1
        arrive_times += 1
        if arrive_times >= 100:
            arrive_times = 0

        # enemy move
        for enemy in enemies:
            enemy.move()
            if time.time() - enemy.start > enemy.interval:
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

        # meteor move
        for meteor in meteors:
            meteor.move()
            if meteor.rect.top > SCREEN_HEIGHT:
                meteors.remove(meteor)
            # meteor hit
            if pygame.sprite.collide_rect(meteor, player):
                meteors.remove(meteor)
                player.is_hit = True

        # gem move
        for gem in gems:
            gem.move()
            if gem.rect.top > SCREEN_HEIGHT:
                gems.remove(gem)
            # gem hit
            if pygame.sprite.collide_rect(gem, player):
                gems.remove(gem)
                scores += 200
                break

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

        # game over event
        if player.is_hit:
            enemies.empty()
            enemies_bullet.empty()
            screen.blit(again, (0, 0))
            plane_collision.play()
            pygame.mixer.music.stop()
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
        gems.draw(screen)
        if scores >= 1000:
            meteors.draw(screen)
            enemy.speed = 2

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
        if key_pressed[K_q]:
            player.moveLeft()
            player.moveUp()
        if key_pressed[K_e]:
            player.moveRight()
            player.moveUp()

        # shoot
        if pygame.mouse.get_pressed()[0] and time.time() - start >= player.interval:
            bullet_img = pygame.image.load('resource/bullet_model/%s.png' % random.randint(12, 20))
            player.shoot(bullet_img)
            bullet_sound.play()
            start = time.time()

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
                        scores += enemy.kind * 5
                    else:
                        enemy.image = enemies_down_img[enemy.kind - 1][enemy.index]
                        enemy.index += 1

       # showScore(scores)

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
        menu(scores)
# start
menu(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # judge if mouse cliked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x = screen.get_rect().centerx
            y = screen.get_rect().centery
            # restart
            if x - 120 <= event.pos[0] and event.pos[0] <= x + 120 and y + 100 >= event.pos[1] and event.pos[1] >= y + 50:
                pygame.mixer.music.stop()
                click_sound.play()
                loading()
                startGame()
            # show the leaderboard
            if x - 120 <= event.pos[0] and event.pos[0] <= x + 120 and y + 50 >= event.pos[1] and event.pos[1] >= y + 10:
                pygame.mixer.music.stop()
                click_sound.play()
                rangking_sound.play()  # play leaderboard bgm
                pygame.display.set_caption('Memoir')
                gameRanking()
            if x - 120 <= event.pos[0] and event.pos[0] <= x + 120 and y + 150 >= event.pos[1] and event.pos[1] >= y + 130:
                click_sound.play()
                pygame.mixer.music.stop()
                time.sleep(1.5)
                exit()
    pygame.display.update()
