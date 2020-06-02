# coding=utf-8

# //////////////////
# ФАЙЛ СПРАЙТОВ
# //////////////////
from const import *
from image import load_image
import random


# =========================
# СПРАЙТ ИГРОКА
# =========================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров игрока определенного размера WIDTH_PLAYER, LENGTH_PLAYER (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_player_img = [load_image(
            os.path.join('static', 'img', 'player',  "player_" + str(i + 1) + '.png'),
            False, (WIDTH_PLAYER, LENGTH_PLAYER)) for i in range(COUNT_PLAYER)]

        # Индекс текущего изображения игрока и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0
        self.image = self.list_player_img[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        # (Для проверок на сталкновения и расположение игрока на экране)
        self.rect = self.image.get_rect()
        self.rect.center = (170, WINDOW_HEIGHT // 2)  # Стартовое расположение игрока на экране

        self.y_speed = 1  # Скорость игрока по y (по x он не будет двигаться)

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения

            if self.index < len(self.list_player_img):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_player_img[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Меняем положение игрока в соответствии с установленным
        self.rect.move_ip((0, self.y_speed))

        # Проверяем на выход за границы экрана
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT


# =========================
# СПРАЙТ ВРАГА
# =========================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, lvl):
        pygame.sprite.Sprite.__init__(self)
        self.list_enemy_img = []  # Создаем пустой список для картинок врага
        # Индекс текущего изображения врага и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        for i in range(COUNT_ENEMY):  # Загружаем картинки
            path_img = os.path.join('static', 'img',  f'level_{lvl}', 'new_enemy',  "enemy_" + str(i + 1) + '.png')
            if lvl in [1, 5, 6, 8]:  # На 1, 5, 6, 8 уровне у нас враги человечки, для них размеры другие
                if i < 10:  # До 10 изображения человечик шагает, следвательно размер изображения меньше
                    self.list_enemy_img.append(load_image(path_img, False, (WIDTH_ENEMY, LENGTH_ENEMY)))
                else:  # После 10 изображения человечик достает оружие, следовательно размер увеличивается
                    self.list_enemy_img.append(load_image(path_img, False,
                                                          (WIDTH_ENEMY_SHOOTING, LENGTH_ENEMY_SHOOTING)))
            else:
                # Для уровней 2, 3, 4, 7, 9 врагом является или танк, или корабль.
                # Их размер идентичен рпзмеру стреляющего человечка, поэтому мы используем размеры стреляющего человечка
                self.list_enemy_img.append(load_image(path_img, False,
                                                      (WIDTH_ENEMY_SHOOTING, LENGTH_ENEMY_SHOOTING)))

        self.image = self.list_enemy_img[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        self.rect = self.image.get_rect()

        # Стартовое расположение врага на экране
        self.rect.center = (WINDOW_WIDTH - WIDTH_ENEMY,
                            random.randint(LENGTH_ENEMY, WINDOW_HEIGHT - LENGTH_ENEMY - 100))
        self.x_speed = 1   # Скорость врага по x (по y он не будет двигаться)
        self.lvl = lvl  # Передаем lvl в update

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения

            # Меняем положение врага и обнуляем скорость смены изображения
            self.x_speed, self.speed_image = -RATE_ENEMY_SPEED, 0

            if self.index == 15:  # Индекс равен 15, это значит, что у человечка кадр стельбы,
                # поэтому мы стеляем на этом кадре
                shooting_enemy.play()  # Включаем звук стельбы
                group_shooting_enemy.add(EnemyShooting(self.rect.midbottom, self.lvl))  # Вызываем класс стрельбы врага

            if self.index < len(self.list_enemy_img):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_enemy_img[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Меняем положение врага в соответствии с установленным
        self.rect.move_ip((self.x_speed, 0))


# =========================
# СПРАЙТ СТРЕЛЬБЫ ИГРОКА
# =========================

class PlayerShooting(pygame.sprite.Sprite):
    def __init__(self, coordinate):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров пуль игрока определенного размера WIDTH_SHOOTING, LENGTH_SHOOTING (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_shooting_img = [load_image(
            os.path.join('static', 'img', 'player_shooting',  "shooting_" + str(i + 1) + '.png'),
            False, (WIDTH_SHOOTING, LENGTH_SHOOTING)) for i in range(COUNT_SHOOTING_PLAYER)]

        # Индекс текущего изображения пули игрока и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        self.image = self.list_shooting_img[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        self.rect = self.image.get_rect()
        self.rect.center = (coordinate[0] + 45, coordinate[1] + 15)  # Стартовое расположение пули игрока на экране

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1  # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения

            if self.index < len(self.list_shooting_img):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_shooting_img[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Проверяем на выход за границы экрана
        if self.rect.right <= WINDOW_WIDTH:
            self.rect.move_ip((5, 0))
        else:
            # Если пуля игрока вышла за границы экрана, то мы удаляем ее
            self.kill()


# =========================
# СПРАЙТ ВЗРЫВА
# =========================

class Explosion(pygame.sprite.Sprite):
    def __init__(self, object_rect):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров взрыва определенного размера WIDTH_EXPLOSION, LENGTH_EXPLOSION (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_explosion_img = [load_image(
            os.path.join('static', 'img', 'animation', "explosion" + str(i + 1) + '.png'),
            False, (WIDTH_EXPLOSION, LENGTH_EXPLOSION)) for i in range(COUNT_EXPLOSION)]

        # Индекс текущего изображения взрыва и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        self.image = self.list_explosion_img[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        self.rect = self.image.get_rect()
        # Стартовое расположение взрыва на экране равно расположению предмета до взрыва
        self.rect.x, self.rect.y = object_rect.x, object_rect.y

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1   # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения

            if self.index < len(self.list_explosion_img):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_explosion_img[self.index]
            else:
                # Индекса нет в длине списка изображений, значит удаляем объект
                self.kill()


# =========================
# СПРАЙТ СТРЕЛЬБЫ ВРАГА
# =========================

class EnemyShooting(pygame.sprite.Sprite):
    def __init__(self, coordinate, lvl):
        pygame.sprite.Sprite.__init__(self)
        # Создаю список кадров пули врага определенного размера WIDTH_SHOOTING_ENEMY, LENGTH_SHOOTING_ENEMY (см. const.py)
        # Функция загрузки изображений находится в image.py
        self.list_shooting_img = [load_image(
            os.path.join('static', 'img',  f'level_{lvl}', 'enemy_shooting',  "shooting_" + str(i + 1) + '.png'),
            False, (WIDTH_SHOOTING_ENEMY, LENGTH_SHOOTING_ENEMY)) for i in range(COUNT_SHOOTING_ENEMY)]

        # Индекс текущего изображения пули врага и начальная скорость смены изображения
        self.index, self.speed_image = -1, 0

        self.image = self.list_shooting_img[self.index]  # Устанавливаю старовое изображение

        # Получаю размеры изображения, квадрат
        self.rect = self.image.get_rect()
        self.rect.center = (coordinate[0] - 15, coordinate[1] - 42)  # Стартовое расположение пули врага на экране

    def update(self):
        self.speed_image += 1  # Увеличиваю скорость смены изображения

        # Если скорость смены изображение больше или ровна задержке смены изображения (5),
        # то сменяем изображение на следующее в списке
        if self.speed_image >= DELAY:
            self.index += 1   # Увеличиваем индекс изображения
            self.speed_image = 0  # Обнуляем скорость смены изображения

            if self.index < len(self.list_shooting_img):  # Проверяем на наличие индекса в длине списка изображений
                # Индекс есть в длине списка изображений, значит устанавливаем новое изображение
                self.image = self.list_shooting_img[self.index]
            else:
                # Индекса нет в длине списка изображений, меняем индекс на начальный
                self.index = -1

        # Проверяем на выход за границы экрана
        if self.rect.bottom <= WINDOW_HEIGHT:
            self.rect.move_ip((-5, 0))
        else:
            # Если пуля врага вышла за границы экрана, то мы удаляем ее
            self.kill()


# =========================
# СПРАЙТ МЕНЮ ИГРОКА
# =========================

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, font, coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.font, self.text = font, text  # Устанавливаем шрифт и текст для передачи в update
        self.image = self.font.render(self.text, True, TEXT_COLOR)  # Устанавливаю старовый текст
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinate  # Получаю координаты

    def update(self):
        self.image = self.font.render(self.text, True, TEXT_COLOR)   # Устанавливаю новый текст


group_shooting_enemy = pygame.sprite.RenderUpdates()  # Создаю группу пуль врага
