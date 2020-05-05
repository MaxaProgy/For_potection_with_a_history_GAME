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
        self.list_player_img = []
        self.index = -1
        self.speed_image = 0
        for i in range(2):  # Загружаем картинки
            path_img = os.path.join('static', 'img', 'level_1', 'player',  "player_" + str(i + 1) + '.png')
            self.list_player_img.append(load_image(path_img, False, (WIDTH_PLAYER, LENGTH_PLAYER)))

        self.image = self.list_player_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (170, WINDOW_HEIGHT // 2)
        self.y_speed = 0  # Перемещение по y

        if self.y_speed == 0:
            self.y_speed = 1

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_player_img):  # Отображаем изображение
                self.image = self.list_player_img[self.index]
            else:
                self.index = -1

        self.rect.move_ip((0, self.y_speed))
        if self.rect.top <= 0:  # Проверка на превышение половины экрана
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
        self.index = -1
        self.speed_image = 0
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
        self.x_speed = 0  # Перемещение по x
        if self.x_speed == 0:
            self.x_speed = 1

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.x_speed = -RATE_ENEMY_SPEED
            self.speed_image = 0
            if self.index == 15:  # Дроид стреляет, только если разрешено
                group_shooting_enemy.add(EnemyShooting(self.rect.midbottom))
            if self.index < len(self.list_enemy_img):  # Отображаем изображение
                self.image = self.list_enemy_img[self.index]
            else:
                self.index = -1
        self.rect.move_ip((self.x_speed, 0))

        if self.rect.left <= 190 or self.rect.right >= WINDOW_WIDTH:
            self.x_speed = -self.x_speed




# =========================
# СПРАЙТ СТРЕЛЬБЫ ИГРОКА
# =========================


class PlayerShooting(pygame.sprite.Sprite):
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.list_shooting_img = []
        self.index = -1
        self.speed_image = 0
        for i in range(4):  # Загружаем картинки
            path_img = os.path.join('static', 'img', 'level_1', 'player_shooting',  "shooting_" + str(i + 1) + '.png')
            self.list_shooting_img.append(load_image(path_img, False, (WIDTH_SHOOTING, LENGTH_SHOOTING)))

        self.image = self.list_shooting_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (p[0] + 45, p[1] + 15)

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_shooting_img):  # Отображаем изображение
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
    def __init__(self, object_rect, type_explosion="explosion"):
        pygame.sprite.Sprite.__init__(self)
        self.index = -1
        self.speed_image = 0
        quantity_image = 7  # Количество изображений, содержащихся в анимации
        self.list_explosion_img = []

        for i in range(0, quantity_image):  # Загружаем картинки
            path_img = os.path.join('static', 'img', 'animation', type_explosion + str(i + 1) + '.png')
            self.list_explosion_img.append(load_image(path_img, False, (WIDTH_EXPLOSION, LENGTH_EXPLOSION)))

        self.image = self.list_explosion_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = object_rect.x
        self.rect.y = object_rect.y

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_explosion_img):  # Отображаем изображение
                self.image = self.list_explosion_img[self.index]
            else:  # Или удаляем объект
                self.kill()


# =========================
# СПРАЙТ СТРЕЛЬБЫ ВРАГА
# =========================


class EnemyShooting(pygame.sprite.Sprite):
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.list_shooting_img = []
        self.index = -1
        self.speed_image = 0
        for i in range(2):  # Загружаем картинки
            path_img = os.path.join('static', 'img', 'level_1', 'enemy_shooting',  "shooting_" + str(i + 1) + '.png')
            self.list_shooting_img.append(load_image(path_img, False, (WIDTH_SHOOTING_ENEMY, LENGTH_SHOOTING_ENEMY)))

        self.image = self.list_shooting_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (p[0] - 15, p[1] - 42)

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.speed_image = 0
            if self.index < len(self.list_shooting_img):  # Отображаем изображение
                self.image = self.list_shooting_img[self.index]
            else:
                self.index = -1
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()
        else:
            self.rect.move_ip((-5, 0))


group_shooting_enemy = pygame.sprite.RenderUpdates()
