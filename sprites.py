# coding=utf-8
from const import *
from image import load_image
import random

# Файл спрайтов

# =========================
# СПРАЙТ ИГРОКА
# =========================


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_player_img = [load_image(
            os.path.join('static', 'img', 'level_1', 'player',  "player_" + str(i + 1) + '.png'),
            False, (WIDTH_PLAYER, LENGTH_PLAYER)) for i in range(2)]

        self.index, self.speed_image = -1, 0
        self.image = self.list_player_img[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (170, WINDOW_HEIGHT // 2)

        self.y_speed = 1

    def update(self):
        self.speed_image += 1
        if self.speed_image >= DELAY_EXPLOSION:
            self.index += 1
            self.speed_image = 0

            if self.index < len(self.list_player_img):
                self.image = self.list_player_img[self.index]
            else:
                self.index = -1
        self.rect.move_ip((0, self.y_speed))
        if self.rect.top <= 0:
            self.rect.top = 0

        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT


# =========================
# СПРАЙТ ВРАГА
# =========================


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_enemy_img = []
        self.index, self.speed_image = -1, 0

        for i in range(17):  # Загружаем картинки
            path_img = os.path.join('static', 'img', 'level_1', 'new_enemy',  "enemy_" + str(i + 1) + '.png')
            if i < 10:
                self.list_enemy_img.append(load_image(path_img, False, (WIDTH_ENEMY, LENGTH_ENEMY)))
            else:
                self.list_enemy_img.append(load_image(path_img, False, (WIDTH_ENEMY_SHOOTING, LENGTH_ENEMY_SHOOTING)))

        self.image = self.list_enemy_img[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH - WIDTH_ENEMY,
                            random.randint(LENGTH_ENEMY, WINDOW_HEIGHT - LENGTH_ENEMY - 100))
        self.x_speed = 1

    def update(self):
        self.speed_image += 1
        if self.speed_image >= DELAY_EXPLOSION:
            self.index += 1
            self.x_speed, self.speed_image = -RATE_ENEMY_SPEED, 0

            if self.index == 15:
                group_shooting_enemy.add(EnemyShooting(self.rect.midbottom))
            if self.index < len(self.list_enemy_img):
                self.image = self.list_enemy_img[self.index]
            else:
                self.index = -1
        self.rect.move_ip((self.x_speed, 0))

        if self.rect.right >= WINDOW_WIDTH:
            self.x_speed = -self.x_speed


# =========================
# СПРАЙТ СТРЕЛЬБЫ ИГРОКА
# =========================


class PlayerShooting(pygame.sprite.Sprite):
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.list_shooting_img = [load_image(
            os.path.join('static', 'img', 'level_1', 'player_shooting',  "shooting_" + str(i + 1) + '.png'),
            False, (WIDTH_SHOOTING, LENGTH_SHOOTING)) for i in range(4)]
        self.index, self.speed_image = -1, 0

        self.image = self.list_shooting_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (p[0] + 45, p[1] + 15)

    def update(self):
        self.speed_image += 1
        if self.speed_image >= DELAY_EXPLOSION:
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_shooting_img):
                self.image = self.list_shooting_img[self.index]
            else:
                self.index = -1

        if self.rect.right <= WINDOW_WIDTH:
            self.rect.move_ip((5, 0))
        else:
            self.kill()


# =========================
# СПРАЙТ ВЗРЫВА
# =========================


class Explosion(pygame.sprite.Sprite):
    def __init__(self, object_rect):
        pygame.sprite.Sprite.__init__(self)
        self.index = -1
        self.speed_image = 0
        self.list_explosion_img = [load_image(
            os.path.join('static', 'img', 'animation', "explosion" + str(i + 1) + '.png'),
            False, (WIDTH_EXPLOSION, LENGTH_EXPLOSION)) for i in range(7)]

        self.image = self.list_explosion_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = object_rect.x, object_rect.y

    def update(self):
        self.speed_image += 1
        if self.speed_image >= DELAY_EXPLOSION:
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_explosion_img):
                self.image = self.list_explosion_img[self.index]
            else:
                self.kill()


# =========================
# СПРАЙТ СТРЕЛЬБЫ ВРАГА
# =========================


class EnemyShooting(pygame.sprite.Sprite):
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.list_shooting_img = [load_image(
            os.path.join('static', 'img', 'level_1', 'enemy_shooting',  "shooting_" + str(i + 1) + '.png'),
                                  False, (WIDTH_SHOOTING_ENEMY, LENGTH_SHOOTING_ENEMY)) for i in range(2)]
        self.index, self.speed_image = -1, 0

        self.image = self.list_shooting_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (p[0] - 15, p[1] - 42)

    def update(self):
        self.speed_image += 1
        if self.speed_image >= DELAY_EXPLOSION:
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_shooting_img):
                self.image = self.list_shooting_img[self.index]
            else:
                self.index = -1
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()
        else:
            self.rect.move_ip((-5, 0))


# =========================
# СПРАЙТ МЕНЮ ИГРОКА
# =========================


class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, font, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.image = self.font.render(self.text, True, TEXTCOLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y

    def update(self):
        self.image = self.font.render(self.text, True, TEXTCOLOR)


group_shooting_enemy = pygame.sprite.RenderUpdates()
