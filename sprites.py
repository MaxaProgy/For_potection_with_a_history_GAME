# coding=utf-8
from const import *
from image import load_image
import random
# Файл спрайтов

# =========================
# СПРАЙТ ИГРОКА
# =========================


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_enemy_img = []
        self.index = -1
        self.speed_image = 0
        for i in range(9):  # Загружаем картинки
            path_img = os.path.join('static', 'img', 'level_1', 'new_enemy',  "enemy_" + str(i + 1) + '.png')
            self.list_enemy_img.append(load_image(path_img, False, (LENGTH_ENEMY, WIDTH_ENEMY)))

        self.image = self.list_enemy_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH - WIDTH_ENEMY,
                            random.randint(LENGTH_ENEMY, WINDOW_HEIGHT - LENGTH_ENEMY - 100))
        self.x_speed = 0  # Перемещение по x
        if self.x_speed == 0:
            self.x_speed = 1
        elif self.y_speed == 0:
            self.y_speed = 1

    def update(self):
        self.speed_image += 1  # Обновляем значение, чтобы изменить изображение
        if self.speed_image >= DELAY_EXPLOSION:  # Меняем изображение каждые 4 кадра
            self.index += 1
            self.x_speed = -RATE_ENEMY_SPEED
            self.speed_image = 0
            if self.index < len(self.list_enemy_img):  # Отображаем изображение
                self.image = self.list_enemy_img[self.index]
            else:
                self.index = -1
        self.rect.move_ip((self.x_speed, 0))

        if self.rect.left <= 190 or self.rect.right >= WINDOW_WIDTH:
            self.x_speed = -self.x_speed
